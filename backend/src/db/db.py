import pymysql
import json
from typing import Dict, Any

def get_db_connection():
    """Get a database connection."""
    return pymysql.connect(
        host='your-db-host',
        user='your-db-user',
        password='your-db-password',
        db='your-db-name',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_backtest_results(backtest_id: int, parameters: Dict[str, Any]):
    """Fetch existing backtest results from the database."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM backtest_results WHERE backtest_id=%s AND parameters=%s"
            cursor.execute(sql, (backtest_id, json.dumps(parameters)))
            result = cursor.fetchone()
            return result
    finally:
        connection.close()

def store_backtest_results(backtest_id: int, parameters: Dict[str, Any], results: Dict[str, Any]):
    """Store new backtest results in the database."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO backtest_results (backtest_id, parameters, results) VALUES (%s, %s, %s)"
            cursor.execute(sql, (backtest_id, json.dumps(parameters), json.dumps(results)))
        connection.commit()
    finally:
        connection.close()
