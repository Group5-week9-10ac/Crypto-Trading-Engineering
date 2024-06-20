import json
from confluent_kafka import Consumer, KafkaError, KafkaException
from config.kafka_config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID

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
                    # End of partition event
                    print(f"Reached end of partition: {msg.partition()}")
                else:
                    raise KafkaException(msg.error())
            else:
                # Message processing
                scene = json.loads(msg.value().decode('utf-8'))
                process_scene(scene)

    except KafkaException as e:
        print(f"Kafka error occurred: {e}")

    except Exception as e:
        print(f"Failed to consume messages: {e}")

    finally:
        consumer.close()

def process_scene(scene):
    """Process and validate the scene for backtesting."""
    try:
        # Extract and validate parameters
        backtest_id = scene.get("backtest_id")
        parameters = scene.get("parameters")

        if not backtest_id or not parameters:
            raise ValueError("Invalid scene: Missing required parameters")

        # Add more validation as necessary
        print(f"Processing backtest ID {backtest_id} with parameters: {parameters}")

        # Initiate backtest process
        initiate_backtest(backtest_id, parameters)

    except ValueError as e:
        print(f"Scene validation failed: {e}")

def initiate_backtest(backtest_id, parameters):
    """Initiate the backtest process using provided parameters."""
    # Placeholder for actual backtest logic
    print(f"Initiating backtest {backtest_id} with parameters: {parameters}")

if __name__ == "__main__":
    backtest_consumer()

