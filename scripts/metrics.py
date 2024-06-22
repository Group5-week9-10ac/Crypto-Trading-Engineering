import sys
import os
import backtrader as bt
import datetime
import json
import math

sys.path.append(os.path.join(os.getcwd(), '/home/jabez/Documents/week_9/Crypto-Trading-Engineering/backtest'))
from backtest import MetricsAnalyzer
from backtest import SMAStrategy 
from backtest import SMAStrategy 
from backtest import EMAStrategy
from backtest import RSIStrategy
from backtest import BollingerBandsStrategy
from backtest import AroonOscillatorStrategy
from backtest import StochasticOscillatorStrategy

import backtest


# Load configuration
with open('backtest_config.json', 'r') as f:
    config = json.load(f)

data_path = config['data_path']
fromdate = datetime.datetime.strptime(config['fromdate'], '%Y-%m-%d')
todate = datetime.datetime.strptime(config['todate'], '%Y-%m-%d')
cash = config['cash']

def execute_backtest(strategy, data_path, fromdate, todate, cash, params):
    # Placeholder function to execute the backtest
    # Replace with actual backtest logic
    print(f"Executing backtest for strategy {strategy.__name__}")
    print(f" From: {fromdate}, To: {todate}, Cash: {cash}, Params: {params}")
    # Add the code to actually run the backtest with the given parameters

def run_strategy(data_path, fromdate, todate, cash):
    best_score = float('-inf')
    best_strategy = None
    
    for strategy_conf in config['strategies']:
        strategy_name = strategy_conf['name']
        params = strategy_conf.get('params', {})
        strategy = globals().get(strategy_name)
        
        if strategy is not None:
            print(f"Running backtest for {strategy_name}")
            score = backtest.run_backtest(strategy, data_path, fromdate, todate, cash, params)
            
            if score is not None and score > best_score:
                score = backtest.run_backtest(strategy, data_path, fromdate, todate, cash, params)
                best_score = score
                best_strategy = strategy_name
        else:
            print(f"Strategy {strategy_name} not found.")
    
    if best_strategy is not None:
        print(f"Best Strategy: {best_strategy} with Score: {best_score:.2f}")
    else:
        print("No valid strategy found.")
        
run_strategy(data_path, fromdate, todate, cash)