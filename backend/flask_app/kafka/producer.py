from confluent_kafka import Producer
import json

def publish_to_kafka(topic, message):
    """
    Publishes a message to a Kafka topic.
    """
    kafka_config = {
        'bootstrap.servers': 'localhost:9092',
        'client.id': 'backtest-producer'
    }

    producer = Producer(kafka_config)
    serialized_message = json.dumps(message)

    try:
        producer.produce(topic, value=serialized_message.encode('utf-8'))
        producer.flush()
        print(f"Published message to Kafka topic '{topic}': {message}")
    except Exception as e:
        print(f"Failed to publish message to Kafka: {e}")
    finally:
        producer.close()

# Example usage (for testing, you can remove this in production)
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
    publish_to_kafka('backtest-results', results)
