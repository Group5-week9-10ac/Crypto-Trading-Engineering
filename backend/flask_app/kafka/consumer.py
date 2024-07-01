from kafka import KafkaConsumer  # Correct import for KafkaConsumer
import json
import os
import sys

# Add the parent directory to the sys.path to ensure proper module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the function for running backtests
from backend.backtest.backtest import run_backtest
from backend.flask_app.kafka.producer import publish_to_kafka
from backend.flask_app.models import db, Scene, BacktestResult
from backend.flask_app.app import save_backtest_results  

# Kafka consumer configuration
bootstrap_servers = ['localhost:9092']
topic_name = 'backtest_scenes'
group_id = 'backtest-group'

# Initialize Kafka consumer
consumer = KafkaConsumer(topic_name,
                         group_id=group_id,
                         bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Consume messages from Kafka
for message in consumer:
    try:
        data = message.value
        print(f"Received message: {data}")

        # Check if results already exist in the database
        existing_results = BacktestResult.query.filter_by(
            scene_id=data['scene_id'],
            from_date=data['fromDate'],
            to_date=data['toDate'],
            strategy_name=data['strategyName']
        ).first()

        if existing_results:
            # Publish existing results to Kafka
            existing_results_data = {
                'scene_id': existing_results.scene_id,
                'strategy_name': existing_results.strategy_name,
                'symbol': existing_results.symbol,
                'from_date': existing_results.from_date.isoformat(),
                'to_date': existing_results.to_date.isoformat(),
                'total_return': existing_results.total_return,
                'trades': existing_results.trades,
                'winning_trades': existing_results.winning_trades,
                'losing_trades': existing_results.losing_trades,
                'max_drawdown': existing_results.max_drawdown,
                'sharpe_ratio': existing_results.sharpe_ratio
            }
            publish_to_kafka('backtest-results', existing_results_data)
        else:
            # Perform backtest and save results
            scene_id = data['scene_id']
            strategy_name = data['strategyName']
            from_date = data['fromDate']
            to_date = data['toDate']
            initial_cash = float(data['initialCash'])
            parameters = data['parameters']

            # Fetch scene details from database
            scene = Scene.query.get(scene_id)
            if not scene:
                print(f"Scene with ID {scene_id} not found in database")
                continue

            # Call your existing backtesting function
            results = run_backtest(scene, from_date, to_date, initial_cash, parameters)

            if results is None:
                print("Backtesting returned None, check input parameters and data availability")
                continue

            # Save results to database
            save_backtest_results(scene_id=scene_id, results=results)

            # Publish results to Kafka
            publish_to_kafka('backtest-results', results)

    except Exception as e:
        print(f"Error processing message: {e}")

# Close consumer connection
consumer.close()
