from confluent_kafka.admin import AdminClient, NewTopic
from config.kafka_config import KAFKA_BOOTSTRAP_SERVERS  # Assuming you define Kafka bootstrap servers in kafka_config.py

def create_kafka_topics():
    """Create Kafka topics if they do not exist."""
    topics = [
        NewTopic("backtest_parameters", num_partitions=1, replication_factor=1),
        # Define more topics as needed
    ]
    
    admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
    admin_client.create_topics(topics)
