import requests
import pandas as pd
from datetime import datetime, timedelta

# Define the CoinGecko API URL
API_URL = 'https://api.coingecko.com/api/v3/coins/markets'
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 100,
    'page': 1,
    'sparkline': 'false'
}

def fetch_crypto_data():
    response = requests.get(API_URL, params=params)
    data = response.json()
    return data

def filter_stable_coins(data):
    stable_coins = ['tether', 'usd-coin', 'binance-usd', 'dai']
    filtered_data = [coin for coin in data if coin['id'] not in stable_coins]
    return filtered_data

def get_top_10_coins(data):
    top_10 = sorted(data, key=lambda x: x['market_cap'], reverse=True)[:10]
    return top_10

# Fetch and process the data
crypto_data = fetch_crypto_data()
filtered_data = filter_stable_coins(crypto_data)
top_10_coins = get_top_10_coins(filtered_data)

# Print the top 10 coins by market cap
for coin in top_10_coins:
    print(f"{coin['name']} - Market Cap: {coin['market_cap']}")

def create_index(top_10_coins):
    total_market_cap = sum(coin['market_cap'] for coin in top_10_coins)
    index = {coin['id']: coin['market_cap'] / total_market_cap for coin in top_10_coins}
    return index

def rebalance_index():
    crypto_data = fetch_crypto_data()
    filtered_data = filter_stable_coins(crypto_data)
    top_10_coins = get_top_10_coins(filtered_data)
    index = create_index(top_10_coins)
    return index

# Initialize the index
index = rebalance_index()
print("Initial Index Weights:", index)

# # Schedule rebalancing every month
# from apscheduler.schedulers.background import BackgroundScheduler

# scheduler = BackgroundScheduler()
# def rebalance_job():
#     index = rebalance_index()
#     print("Rebalanced Index Weights:", index)

# # Schedule the rebalance job every month
# scheduler.add_job(rebalance_job, 'interval', days=30)
# scheduler.start()

# try:
#     # Keep the script running
#     while True:
#         pass
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()
