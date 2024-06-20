from typing import List
from confluent_kafka.admin import AdminClient, NewTopic, KafkaException
from config.kafka_config import KAFKA_BOOTSTRAP_SERVERS

def create_kafka_topics(topic_names: List[str]) -> None:
    """Create Kafka topics if they do not exist."""
    new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topic_names]

    admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

    try:
        # Ensure topics are created asynchronously
        admin_client.create_topics(new_topics, operation_timeout=30)
        print("Kafka topics created successfully.")

    except KafkaException as kafka_exception:
        print(f"Kafka Exception: {kafka_exception}")

    except Exception as e:
        print(f"Failed to create Kafka topics: {e}")

# Example usage
if __name__ == "__main__":
    topics_to_create = [
        "crypto_prices",
        "backtest_parameters",
        "backtest_results",
        "trading_signals",
        "portfolio_management",
        "market_news",
        "risk_management",
        "order_execution"
    ]

    create_kafka_topics(topics_to_create)
