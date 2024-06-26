from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import psycopg2
import os
import sys
import pandas as pd
import torch
from chronos import ChronosPipeline
import plotly.graph_objs as go
import numpy as np

sys.path.append(os.path.join(os.getcwd(), '/home/jabez_kassa/week_9/Crypto-Trading-Engineering/scripts'))
import coins, portfolio, forecast, db_conn

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Establish a database connection
try:
    conn = psycopg2.connect(
        dbname="historical_data",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    logging.info("Database connection established")
except Exception as e:
    logging.error(f"Failed to connect to the database: {e}")
    raise

# Load data from the database into DataFrames
try:
    coin_data = {
        'BTC': db_conn.get_df_from_db(conn, 'btc_data'),
        'ETH': db_conn.get_df_from_db(conn, 'eth_data'),
        'BNB': db_conn.get_df_from_db(conn, 'bnb_data'),
        'SOL': db_conn.get_df_from_db(conn, 'sol_data'),
        'XRP': db_conn.get_df_from_db(conn, 'xrp_data')
    }
    logging.info("DataFrames loaded successfully from the database")
except Exception as e:
    logging.error(f"Failed to load data from the database: {e}")
    raise

@app.route("/results")
def results():
    try:
        df = coins.coins_df()
        logging.debug(f"DataFrame for coins: {df.head()}")
        portfolio_result = portfolio.ef_portfolio(df)
        return jsonify(portfolio_result)
    except Exception as e:
        logging.error(f"Error in /results: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/results2")
def results2():
    try:
        df = coins.coins_df()
        logging.debug(f"DataFrame for coins: {df.head()}")
        portfolio_result2 = portfolio.lowrisk_porfolio(df)
        return jsonify(portfolio_result2)
    except Exception as e:
        logging.error(f"Error in /results2: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/forecasts")
def forecasts():
    try:
        coin = request.args.get('coin', 'BTC')  # Default to 'BTC' if no coin is specified

        # Reload DataFrame from the original data source
        df = db_conn.get_df_from_db(conn, f'{coin.lower()}_data')

        if df is None or df.empty:
            logging.error(f"Data for the selected coin '{coin}' does not exist or is empty")
            return jsonify({"error": f"Data for the selected coin '{coin}' does not exist"}), 404

        # Prepare the data and context
        context = forecast.data_preparation(df)
        forecast_dates = forecast.generate_forecast_dates(df)
        forecast_fig = forecast.predict(coin, df, forecast_dates, context)

        # Convert Plotly figure to JSON for passing to front-end
        forecast_json = forecast_fig.to_json()

        return jsonify(forecast_json)

    except Exception as e:
        logging.error(f"Error in /forecasts: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
