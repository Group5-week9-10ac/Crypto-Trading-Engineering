import json
from typing import Dict, Any
import backtrader as bt 
import psycopg2
from confluent_kafka import Consumer, KafkaError, KafkaException
from backend.src.config.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID
from config.config import DATABASE_CONFIG
from services.backtest_service import initiate_backtest

def backtest_consumer():
    """Kafka consumer to process backtest parameters."""
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['backtest_parameters'])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"Reached end of partition: {msg.partition()}")
                else:
                    raise KafkaException(msg.error())
            else:
                scene = json.loads(msg.value().decode('utf-8'))
                process_scene(scene)

    except KafkaException as e:
        print(f"Kafka error occurred: {e}")
        # Implement retry mechanism or error handling strategy for Kafka errors
    
    except Exception as e:
        print(f"Failed to consume messages: {e}")
        # Handle other exceptions as needed
    
    finally:
        consumer.close()

def process_scene(scene):
    """Process and validate the scene for backtesting."""
    try:
        backtest_id = scene.get("backtest_id")
        parameters = scene.get("parameters")

        if not backtest_id or not parameters:
            raise ValueError("Invalid scene: Missing required parameters")

        print(f"Processing backtest ID {backtest_id} with parameters: {parameters}")

        if check_existing_results(parameters):
            print("Existing results found. Fetching from database...")
            results = fetch_results(parameters)
        else:
            print("No existing results. Initiating backtest...")
            results = initiate_backtest(backtest_id, parameters)
            store_results(backtest_id, parameters, results)

        print(f"Results: {results}")

    except ValueError as e:
        print(f"Scene validation failed: {e}")

def check_existing_results(parameters):
    """Check if backtest results already exist in the database."""
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        query = """
        SELECT COUNT(*) FROM backtest_results
        WHERE parameters = %s
        """
        cursor.execute(query, (json.dumps(parameters),))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return False

def fetch_results(parameters):
    """Fetch existing backtest results from the database."""
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        query = """
        SELECT results FROM backtest_results
        WHERE parameters = %s
        """
        cursor.execute(query, (json.dumps(parameters),))
        results = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return results
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

def store_results(backtest_id, parameters, results):
    """Store new backtest results in the database."""
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        query = """
        INSERT INTO backtest_results (backtest_id, parameters, results)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (backtest_id, json.dumps(parameters), json.dumps(results)))
        conn.commit()
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    backtest_consumer()

