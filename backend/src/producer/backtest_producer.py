import json
from typing import List, Dict
from confluent_kafka import Producer, KafkaException
from confluent_kafka.admin import NewTopic
from config.kafka_config import KAFKA_BOOTSTRAP_SERVERS

def delivery_report(err: KafkaException, msg: str) -> None:
    """Delivery report callback."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_backtest_parameters(scenes: List[Dict[str, any]]) -> None:
    """Publish scenes (backtest parameters) to Kafka topic."""
    producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

    try:
        # Produce each scene as a JSON-encoded message
        for scene in scenes:
            producer.produce(
                "backtest_parameters",
                json.dumps(scene).encode('utf-8'),
                callback=delivery_report
            )
        
    except KafkaException as kafka_exception:
        print(f"Kafka Error: {kafka_exception}")
    
    except Exception as e:
        print(f"Failed to publish scenes to Kafka: {e}")
    
    finally:
        producer.flush()

# Example usage
if __name__ == "__main__":
    scenes = [
        {"backtest_id": 1, "parameters": {"indicator": "moving_average", "date_range": "2023-01-01 to 2023-06-30"}},
        {"backtest_id": 2, "parameters": {"indicator": "rsi", "date_range": "2023-01-01 to 2023-06-30"}},
        # Add more scenes as needed
    ]

    produce_backtest_parameters(scenes)