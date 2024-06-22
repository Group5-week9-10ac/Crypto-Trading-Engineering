import json
from confluent_kafka import Consumer, KafkaError, KafkaException
from backend.src.config.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID
from dotenv import load_dotenv
from services.backtest_service import initiate_backtest
import os
from db.db import get_db_connection, fetch_backtest_results, store_backtest_results
from producer.backtest_producer import produce_backtest_results

# Load environment variables from .env file
load_dotenv()

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

            # Commit offsets manually after processing each message
            consumer.commit()

    except KafkaException as e:
        print(f"Kafka error occurred: {e}")
        # Implement retry or alert mechanism here
    except Exception as e:
        print(f"Failed to consume messages: {e}")
        # Implement retry or alert mechanism here
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

        # Fetch results from the database
        results = fetch_backtest_results(backtest_id, parameters)

        if results:
            print("Existing results found. Publishing to Kafka...")
            produce_backtest_results(results)
        else:
            print("No existing results. Initiating backtest...")
            results = initiate_backtest(backtest_id, parameters)
            store_backtest_results(backtest_id, parameters, results)

            # Publish the new results to Kafka
            produce_backtest_results(results)

        print(f"Results: {results}")

    except ValueError as e:
        print(f"Scene validation failed: {e}")
    except Exception as e:
        print(f"Failed to process scene: {e}")
        # Implement retry or alert mechanism here

if __name__ == "__main__":
    backtest_consumer()
