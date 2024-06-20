import json
import psycopg2
from psycopg2 import pool
from confluent_kafka import Consumer, KafkaError, KafkaException
from backend.src.config.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID
from dotenv import load_dotenv
from services.backtest_service import initiate_backtest
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve database configuration from environment variables
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT', '5432')  # Adjust port if necessary
}

# Initialize connection pool for PostgreSQL
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **DATABASE_CONFIG
)

def get_db_connection():
    """Get a connection from the connection pool."""
    return db_pool.getconn()

def release_db_connection(conn):
    """Release the connection back to the pool."""
    db_pool.putconn(conn)

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

        if check_existing_results(parameters):
            print("Existing results found. Fetching from database...")
            results = fetch_results(parameters)
        else:
            print("No existing results. Initiating backtest...")
            results = initiate_backtest(backtest_id, parameters)
            store_results(backtest_id, parameters, results)

        print(f"Results: {results}")

    except ValueError as e:
        print(f"Scene validation failed: {e}")
    except Exception as e:
        print(f"Failed to process scene: {e}")
        # Implement retry or alert mechanism here

def check_existing_results(parameters):
    """Check if backtest results already exist in the database."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT COUNT(*) FROM backtest_results
            WHERE parameters = %s
            """
            cursor.execute(query, (json.dumps(parameters),))
            count = cursor.fetchone()[0]
        return count > 0
    finally:
        release_db_connection(conn)

def fetch_results(parameters):
    """Fetch existing backtest results from the database."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT results FROM backtest_results
            WHERE parameters = %s
            """
            cursor.execute(query, (json.dumps(parameters),))
            results = cursor.fetchone()[0]
        return results
    finally:
        release_db_connection(conn)

def store_results(backtest_id, parameters, results):
    """Store new backtest results in the database."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = """
            INSERT INTO backtest_results (backtest_id, parameters, results)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (backtest_id, json.dumps(parameters), json.dumps(results)))
            conn.commit()
    finally:
        release_db_connection(conn)

if __name__ == "__main__":
    backtest_consumer()
