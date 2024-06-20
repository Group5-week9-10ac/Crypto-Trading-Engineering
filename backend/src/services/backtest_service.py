import json
from typing import Dict, Any
import backtrader as bt 
from db.db import get_db_connection, fetch_backtest_results, store_backtest_results

def process_scene(scene: Dict[str, Any]):
    """Process and validate the scene for backtesting."""
    try:
        # Extract and validate parameters
        backtest_id = scene.get("backtest_id")
        parameters = scene.get("parameters")

        if not backtest_id or not parameters:
            raise ValueError("Invalid scene: Missing required parameters")

        # Add more validation as necessary
        print(f"Processing backtest ID {backtest_id} with parameters: {parameters}")

        # Initiate backtest process
        initiate_backtest(backtest_id, parameters)

    except ValueError as e:
        print(f"Scene validation failed: {e}")

def initiate_backtest(backtest_id: int, parameters: Dict[str, Any]):
    """Initiate the backtest process using provided parameters."""
    # Check if results already exist
    existing_results = fetch_backtest_results(backtest_id, parameters)
    
    if existing_results:
        print(f"Results already exist for backtest ID {backtest_id}. Fetching from database.")
        return existing_results

    # If not, run the backtest
    print(f"Running new backtest for ID {backtest_id} with parameters: {parameters}")
    
    # Placeholder for actual backtest logic using Backtrader or any other framework
    cerebro = bt.Cerebro()
    # Add your data feed and strategy to cerebro here
    # ...
    
    result = cerebro.run()
    
    # Extract and format the results
    backtest_results = {
        "return": result[0].analyzers.returns.get_analysis(),  # Example, adjust as necessary
        "number_of_trades": result[0].analyzers.trades.get_analysis(),
        # Add other metrics
    }
    
    # Store results in the database
    store_backtest_results(backtest_id, parameters, backtest_results)

    return backtest_results
