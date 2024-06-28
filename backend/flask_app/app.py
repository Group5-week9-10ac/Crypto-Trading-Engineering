from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import os
import sys
import logging
from kafka import KafkaConsumer

# Add the parent directory to the sys.path to ensure proper module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the function for running backtests
from backend.backtest.backtest import run_backtest
from backend.flask_app.kafka.producer import publish_to_kafka
from backend.flask_app.config import Config
from backend.flask_app.models import db, Scene, BacktestResult

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Kafka configuration
KAFKA_BROKER_URL = 'localhost:9092'
KAFKA_TOPIC = 'backtest_scenes'

# Kafka consumer setup
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Function to consume scenes from Kafka
def consume_scenes():
    for message in consumer:
        scene_data = message.value
        print(f"Received scene from Kafka: {scene_data}")

        # Extract necessary data from scene_data
        scene_id = scene_data['scene_id']
        strategy_name = scene_data['strategyName']
        from_date = scene_data['fromDate']
        to_date = scene_data['toDate']
        initial_cash = float(scene_data['initialCash'])
        parameters = {
            'indicator': scene_data['parameters']['indicator'],
            'indicator_period': int(scene_data['parameters']['indicatorPeriod']),
            'symbol': scene_data['parameters']['symbol']
        }

        # Fetch scene details from database
        scene = Scene.query.get(scene_id)
        if not scene:
            print(f"Scene with ID {scene_id} not found in database")
            continue

        # Call your existing backtesting function
        results = run_backtest(scene, from_date, to_date, initial_cash, parameters)

        # If results is None, handle the error
        if results is None:
            print("Backtesting returned None, check input parameters and data availability")
            continue

        # Save results to database
        save_backtest_results(scene_id=scene_id, results=results)

        # Publish results to Kafka
        publish_to_kafka(results)

# Routes
@app.route('/')
def index():
    scenes = Scene.query.all()
    return render_template('index.html', scenes=scenes)

@app.route('/api/run_backtest', methods=['POST'])
def api_run_backtest():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debugging print to check received JSON

        # Extract data from JSON
        scene_id = data['scene_id']
        strategy_name = data['strategyName']
        from_date = data['fromDate']
        to_date = data['toDate']
        initial_cash = float(data['initialCash'])
        parameters = {
            'indicator': data['parameters']['indicator'],
            'indicator_period': int(data['parameters']['indicator_period']),  # Ensure indicator_period is converted to int
            'symbol': data['parameters']['symbol']
        }

        # Fetch scene details from database
        scene = Scene.query.get(scene_id)
        if not scene:
            raise ValueError(f"Scene with ID {scene_id} not found in database")

        # Call your existing backtesting function
        results = run_backtest(scene, from_date, to_date, initial_cash, parameters)

        # If results is None, handle the error
        if results is None:
            raise ValueError("Backtesting returned None, check input parameters and data availability")

        # Save results to database
        save_backtest_results(scene_id=scene_id, results=results)

        # Publish results to Kafka
        publish_to_kafka(results)

        # Return the results
        return jsonify({
            'status': 'success',
            'results': results
        })

    except Exception as e:
        print(f"Error running backtest: {e}")
        return jsonify({'error': f"Error running backtest: {e}"}), 500

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

def save_backtest_results(scene_id, results):
    try:
        # Save results to BacktestResult table
        result = BacktestResult(
            scene_id=scene_id,
            strategy_name=results['strategy_name'],
            symbol=results['symbol'],
            from_date=results['from_date'],
            to_date=results['to_date'],
            total_return=results['total_return'],
            trades=results['trades'],
            winning_trades=results['winning_trades'],
            losing_trades=results['losing_trades'],
            max_drawdown=results['max_drawdown'],
            sharpe_ratio=results['sharpe_ratio']
        )
        db.session.add(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving backtest results: {e}")

if __name__ == "__main__":
    # Start Kafka consumer as a background process
    from threading import Thread
    consumer_thread = Thread(target=consume_scenes)
    consumer_thread.daemon = True
    consumer_thread.start()

    # Start Flask app
    app.run(debug=True)
