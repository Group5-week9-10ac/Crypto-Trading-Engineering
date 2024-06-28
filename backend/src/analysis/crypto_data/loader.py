from typing import Any
import pandas as pd
from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import SQLAlchemyError

from config import load_config
from exceptions import DataLoaderError, DatabaseConnectionError, DataInsertionError


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        data['Date'] = pd.to_datetime(data['Date'])
        data.columns = map(str.lower, data.columns)  # Convert column names to lowercase
        data.rename(columns={
            'date': 'date',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'dividends': 'dividends',
            'stock splits': 'stock_splits'  # Ensure correct column name for database
        }, inplace=True)
        return data
    except Exception as e:
        raise DataLoaderError(f"Error loading data from {file_path}: {e}")

def get_database_engine(config: dict) -> Engine:
    """
    Create a database engine using the provided configuration.

    Args:
        config (dict): A dictionary containing database configurations.

    Returns:
        Engine: A SQLAlchemy Engine instance.
    """
    try:
        connection_string = f"postgresql://{config['POSTGRES_USER']}:{config['POSTGRES_PASSWORD']}@" \
                            f"{config['POSTGRES_HOST']}:{config['POSTGRES_PORT']}/{config['POSTGRES_DB']}"
        engine = create_engine(connection_string)
        return engine
    except SQLAlchemyError as e:
        raise DatabaseConnectionError(f"Error connecting to the database: {e}")

def insert_data(engine: Engine, data: pd.DataFrame, table_name: str) -> None:
    """
    Insert data into the specified database table.

    Args:
        engine (Engine): The SQLAlchemy Engine instance.
        data (pd.DataFrame): The data to insert.
        table_name (str): The name of the table to insert data into.
    """
    try:
        data.to_sql(table_name, engine, if_exists='append', index=False)
    except SQLAlchemyError as e:
        raise DataInsertionError(f"Error inserting data into {table_name}: {e}")

def main() -> None:
    """
    Main function to load data and insert it into the PostgreSQL database.
    """
    try:
        config = load_config()
        engine = get_database_engine(config)
        
        # Load BTC and ETH data
        btc_data = load_data('/home/moraa/Documents/10_academy/Week-9/Crypto-Trading-Engineering/MLOps/backend/notebooks/btc_data.csv')
        eth_data = load_data('/home/moraa/Documents/10_academy/Week-9/Crypto-Trading-Engineering/MLOps/backend/notebooks/eth_data.csv')
        
        # Insert data into the database
        insert_data(engine, btc_data, 'btc_data')
        insert_data(engine, eth_data, 'eth_data')
        
        print("Data inserted successfully.")
    except DataLoaderError as e:
        print(e)

if __name__ == "__main__":
    main()
