from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import requests
import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def get_backtest_config() -> Dict[str, Any]:
    """
    Returns the configuration dictionary for the backtest.

    Returns:
        dict: Configuration dictionary for the backtest.
    """
    return {
        "scene_id": 1,
        "strategyName": "SMAStrategy",
        "fromDate": "2023-01-01",
        "toDate": "2023-05-01",
        "initialCash": "10000",
        "parameters": {
            "indicator": "sma",
            "indicator_period": "20",
            "symbol": "btc"
        }
    }

def send_backtest_request(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sends a POST request to the backtest API with the given configuration.

    Args:
        config (dict): Configuration dictionary for the backtest.

    Returns:
        dict: JSON response from the API.
    
    Raises:
        RequestException: If the HTTP request fails.
    """
    url = 'http://localhost:5000/api/run_backtest'
    try:
        response = requests.post(url, json=config)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        logger.error("Failed to send backtest request: %s", e)
        raise

def run_backtest(**kwargs: Any) -> None:
    """
    Orchestrates the backtest by retrieving the configuration and sending a request to the API.

    Args:
        **kwargs: Arbitrary keyword arguments (required for Airflow tasks).
    
    Raises:
        Exception: If the backtest request fails.
    """
    try:
        config = get_backtest_config()
        result = send_backtest_request(config)
        logger.info("Backtest result: %s", result)
    except Exception as e:
        logger.error("Error occurred during backtest: %s", e)
        raise

# Define the DAG
dag = DAG(
    'backtest_dag',
    default_args=default_args,
    description='A DAG to run a backtest API call.',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
)

# Define the task using PythonOperator
run_backtest_task = PythonOperator(
    task_id='run_backtest',
    python_callable=run_backtest,
    provide_context=True,
    dag=dag,
)
