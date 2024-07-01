from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from kafka import KafkaConsumer
from threading import Thread
import json
import os
import sys
import logging
from typing import Dict, Any

# Add the parent directory to the sys.path to ensure proper module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import application components
from backend.backtest.backtest import run_backtest
from backend.flask_app.kafka.producer import publish_to_kafka
from backend.flask_app.config import Config
from backend.flask_app.models import db, Scene, BacktestResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

def create_consumer(topic: str, broker_url: str) -> KafkaConsumer:
    """
    Create and return a Kafka consumer for the given topic and broker URL.

    Args:
        topic (str): The Kafka topic to consume messages from.
        broker_url (str): The Kafka broker URL.

    Returns:
        KafkaConsumer: Configured KafkaConsumer instance.
    """
    return KafkaConsumer(
        topic,
        bootstrap_servers=broker_url,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def consume_scenes(consumer: KafkaConsumer) -> None:
    """
    Consume messages from Kafka and process them.

    Args:
        consumer (KafkaConsumer): KafkaConsumer instance to consume messages from.
    """
    for message in consumer:
        scene_data = message.value
        logger.info(f"Received scene from Kafka: {scene_data}")

        try:
            # Extract necessary data from scene_data
            scene_id = scene_data['scene_id']
            strategy_name = scene_data['strategyName']
            from_date = scene_data['fromDate']
            to_date = scene_data['toDate']
            initial_cash = float(scene_data['initialCash'])
            parameters = scene_data['parameters']

            # Fetch scene details from database
            scene = Scene.query.get(scene_id)
            if not scene:
                logger.warning(f"Scene with ID {scene_id} not found in database")
                continue

            # Call backtesting function
            results = run_backtest(scene, from_date, to_date, initial_cash, parameters)

            if results is None:
                logger.warning("Backtesting returned None, check input parameters and data availability")
                continue

            # Save results and publish them
            save_backtest_results(scene_id, results)
            publish_to_kafka(results)

        except Exception as e:
            logger.error(f"Error processing Kafka message: {e}")

def save_backtest_results(scene_id: int, results: Dict[str, Any]) -> None:
    """
    Save backtest results to the database.

    Args:
        scene_id (int): The ID of the scene for which results are saved.
        results (Dict[str, Any]): The backtest results to be saved.

    Raises:
        Exception: If an error occurs while saving the results.
    """
    try:
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
        logger.error(f"Error saving backtest results: {e}")

@app.route('/')
def index() -> str:
    """
    Render the index page with a list of scenes.

    Returns:
        str: Rendered HTML for the index page.
    """
    scenes = Scene.query.all()
    return render_template('index.html', scenes=scenes)

@app.route('/api/run_backtest', methods=['POST'])
def api_run_backtest() -> Any:
    """
    Handle backtest request and return results.

    Returns:
        Any: JSON response containing the status and results or error message.
    """
    try:
        data = request.get_json()
        logger.info(f"Received data: {data}")

        # Extract data from JSON
        scene_id = data['scene_id']
        strategy_name = data['strategyName']
        from_date = data['fromDate']
        to_date = data['toDate']
        initial_cash = float(data['initialCash'])
        parameters = data['parameters']

        # Check if backtest results already exist
        existing_results = BacktestResult.query.filter_by(
            scene_id=scene_id,
            strategy_name=strategy_name,
            from_date=from_date,
            to_date=to_date
        ).first()

        if existing_results:
            logger.info("Fetching existing backtest results from database.")
            return jsonify({
                'status': 'success',
                'results': existing_results.serialize()  # Assumes you have a serialize method in BacktestResult
            })

        # Fetch scene details from database
        scene = Scene.query.get(scene_id)
        if not scene:
            raise ValueError(f"Scene with ID {scene_id} not found in database")

        # Call backtesting function
        results = run_backtest(scene, from_date, to_date, initial_cash, parameters)

        if results is None:
            raise ValueError("Backtesting returned None, check input parameters and data availability")

        # Save results and publish them
        save_backtest_results(scene_id, results)
        publish_to_kafka(results)

        return jsonify({
            'status': 'success',
            'results': results
        })

    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        return jsonify({'error': f"Error running backtest: {e}"}), 500

@app.route('/favicon.ico')
def favicon() -> str:
    """
    Serve the favicon file.

    Returns:
        str: Path to the favicon file.
    """
    return app.send_static_file('favicon.ico')

if __name__ == "__main__":
    kafka_consumer = create_consumer(Config.KAFKA_TOPIC, Config.KAFKA_BROKER_URL)
    consumer_thread = Thread(target=consume_scenes, args=(kafka_consumer,))
    consumer_thread.daemon = True
    consumer_thread.start()

    app.run(debug=True)
