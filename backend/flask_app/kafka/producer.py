from confluent_kafka import Producer
import json

def publish_to_kafka(results):
    """
    Publishes backtest results to Kafka topic.
    Assumes 'results' is a dictionary containing backtest results.
    """
    # Kafka configuration
    kafka_config = {
        'bootstrap.servers': 'localhost:9092',  # Kafka broker address
        'client.id': 'backtest-producer'
    }

    # Create Kafka producer
    producer = Producer(kafka_config)

    # Define Kafka topic
    kafka_topic = 'backtest-results'

    # Serialize results to JSON before publishing
    serialized_results = json.dumps(results)

    # Publish results to Kafka
    try:
        producer.produce(kafka_topic, value=serialized_results.encode('utf-8'))
        producer.flush()
        print(f"Published backtest results to Kafka: {results}")
    except Exception as e:
        print(f"Failed to publish backtest results to Kafka: {e}")
    finally:
        producer.close()

# Example usage (you can remove this in your actual production code)
if __name__ == "__main__":
    results = {
        'strategy_name': 'SMA Strategy',
        'symbol': 'BTC/USD',
        'from_date': '2024-06-01',
        'to_date': '2024-06-30',
        'total_return': 0.05,
        'trades': 100,
        'winning_trades': 60,
        'losing_trades': 40,
        'max_drawdown': 0.02,
        'sharpe_ratio': 1.5
    }
    publish_to_kafka(results)
