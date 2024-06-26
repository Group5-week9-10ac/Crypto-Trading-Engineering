import requests
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.join(os.getcwd(), '/home/jabez_kassa/week_9/Crypto-Trading-Engineering/scripts'))
import index_fund
def coins_df():
    df_btc = pd.read_csv('/home/jabez_kassa/week_9/Crypto-Trading-Engineering/data/BTC-USD.csv')
    df_eth= pd.read_csv('/home/jabez_kassa/week_9/Crypto-Trading-Engineering/data/ETH-USD.csv')
    df_bnb= pd.read_csv('/home/jabez_kassa/week_9/Crypto-Trading-Engineering/data/BNB-USD.csv')
    df_sol= pd.read_csv('/home/jabez_kassa/week_9/Crypto-Trading-Engineering/data/SOL-USD.csv')
    df_xrp= pd.read_csv('/home/jabez_kassa/week_9/Crypto-Trading-Engineering/data/XRP-USD.csv')

    df_btc = df_btc[['Date', 'Close']].rename(columns={'Close': 'btc_price'})
    df_eth = df_eth[['Date', 'Close']].rename(columns={'Close': 'eth_price'})
    df_bnb = df_bnb[['Date', 'Close']].rename(columns={'Close': 'bnb_price'})
    df_sol = df_sol[['Date', 'Close']].rename(columns={'Close': 'sol_price'})
    df_xrp = df_xrp[['Date', 'Close']].rename(columns={'Close': 'xrp_price'})

    # Merge data frames on 'Date' column
    df = df_btc.merge(df_eth, on='Date').merge(df_bnb, on='Date').merge(df_sol, on='Date').merge(df_xrp, on='Date')

    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)

    # Convert all other columns to numeric, coerce errors to NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    return df