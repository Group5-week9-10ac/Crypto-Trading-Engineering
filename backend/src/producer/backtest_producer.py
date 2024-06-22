import json
from typing import Dict
from confluent_kafka import Producer, KafkaException, Message
from backend.src.config.config import KAFKA_BOOTSTRAP_SERVERS

def delivery_report(err: KafkaException, msg: Message) -> None:
    """Delivery report callback."""
    if err is not None:
        print(f"Message delivery failed: {err}")
        # Implement retry mechanism or error handling strategy here
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_backtest_results(results: Dict[str, any]) -> None:
    """Publish backtest results to Kafka topic."""
    producer = Producer({
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        # Additional Kafka producer configurations for reliability and scalability
        "acks": "all",            # Ensure all replicas acknowledge message delivery
        "retries": 3,             # Retry failed message delivery up to 3 times
        "delivery.timeout.ms": 10000  # Timeout for message delivery
    })

    try:
        # Produce the results as a JSON-encoded message
        producer.produce(
            "backtest_results",
            json.dumps(results).encode('utf-8'),
            callback=delivery_report
        )
        
    except KafkaException as kafka_exception:
        print(f"Kafka Error: {kafka_exception}")
        # Implement error handling strategy, such as retry logic or logging
    
    except Exception as e:
        print(f"Failed to publish results to Kafka: {e}")
        # Handle other exceptions as needed
    
    finally:
        producer.flush()  # Ensure all messages are delivered before closing producer

    # Close the producer after flushing all messages
    producer.close()


