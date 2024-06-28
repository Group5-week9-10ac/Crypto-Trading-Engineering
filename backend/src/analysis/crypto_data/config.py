import os
from dotenv import load_dotenv

def load_config(dotenv_path: str = '/home/moraa/Documents/10_academy/Week-9/Crypto-Trading-Engineering/MLOps/.env') -> dict:
    """
    Load environment variables from a .env file.
    
    Args:
        dotenv_path (str): Path to the .env file.

    Returns:
        dict: A dictionary containing database configurations.
    """
    load_dotenv(dotenv_path)
    
    config = {
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'POSTGRES_DB': os.getenv('POSTGRES_DB'),
        'POSTGRES_HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'POSTGRES_PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
    
    return config
