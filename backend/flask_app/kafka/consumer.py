from kafka import KafkaConsumer
import json
from app import db, BacktestResult  # Assuming db and BacktestResult are defined in your Flask app

# Kafka consumer configuration
bootstrap_servers = ['localhost:9092']
topic_name = 'backtest-results'
group_id = 'backtest-group'

# Initialize Kafka consumer
consumer = KafkaConsumer(topic_name,
                         group_id=group_id,
                         bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Consume messages from Kafka
for message in consumer:
    try:
        # Process the message
        data = message.value
        print(f"Received message: {data}")

        # Example: Save backtest result to database
        result = BacktestResult(
            scene_id=data['scene_id'],
            strategy_name=data['strategy_name'],
            symbol=data['symbol'],
            from_date=data['from_date'],
            to_date=data['to_date'],
            total_return=data['total_return'],
            trades=data['trades'],
            winning_trades=data['winning_trades'],
            losing_trades=data['losing_trades'],
            max_drawdown=data['max_drawdown'],
            sharpe_ratio=data['sharpe_ratio']
        )
        db.session.add(result)
        db.session.commit()

        print("Saved backtest result to database.")

    except Exception as e:
        print(f"Error processing message: {e}")

# Close consumer connection
consumer.close()
