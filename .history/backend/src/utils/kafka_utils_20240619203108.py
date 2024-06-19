from confluent_kafka.admin import AdminClient, NewTopic
from config.kafka_config import KAFKA_BOOTSTRAP_SERVERS

def create_kafka_topics():
    """Create Kafka topics if they do not exist."""
    topics = [
        "crypto_prices",
        "backtest_parameters",
        "backtest_results",
        "trading_signals",
        "portfolio_management",
        "market_news",
        "risk_management",
        "order_execution"
    ]
    
    new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics]
    
    admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
    admin_client.create_topics(new_topics)

