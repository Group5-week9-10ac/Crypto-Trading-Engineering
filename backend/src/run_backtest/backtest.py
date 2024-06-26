import psycopg2
import pandas as pd
import backtrader as bt
import datetime
import json
import math
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Metrics analyzer
class MetricsAnalyzer(bt.Analyzer):
    def start(self):
        self.returns = []
        self.trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.drawdown = 0
        self.max_drawdown = 0
        self.sharpe_ratio = 0

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trades += 1
            if trade.pnl > 0:
                self.winning_trades += 1
            else:
                self.losing_trades += 1

    def next(self):
        portfolio_value = self.strategy.broker.getvalue()
        self.returns.append(portfolio_value)

    def stop(self):
        # Calculate total return
        initial_value = self.returns[0] if self.returns else 0
        final_value = self.returns[-1] if self.returns else 0
        total_return = (final_value - initial_value) / initial_value if initial_value else 0

        # Calculate Sharpe Ratio
        if len(self.returns) > 1:
            avg_return = sum(self.returns) / len(self.returns)
            stddev = math.sqrt(sum((r - avg_return) ** 2 for r in self.returns) / len(self.returns))
            self.sharpe_ratio = avg_return / stddev if stddev else 0

        # Calculate Max Drawdown
        peak = self.returns[0]
        for value in self.returns:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak if peak else 0
            if drawdown > self.max_drawdown:
                self.max_drawdown = drawdown

        # Store metrics in strategy object
        self.strategy.metrics = {
            'total_return': total_return * 100,
            'trades': self.trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'max_drawdown': self.max_drawdown * 100,
            'sharpe_ratio': self.sharpe_ratio
        }

        # Insert results into PostgreSQL
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host='localhost'
            )
            cur = conn.cursor()

            query = """
            INSERT INTO backtest_results (strategy_name, symbol, from_date, to_date, total_return, trades, winning_trades, losing_trades, max_drawdown, sharpe_ratio)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (
                self.strategy.__class__.__name__, 
                'btc', 
                config['fromdate'],  # Use fromdate from the loaded config
                config['todate'],    # Use todate from the loaded config
                self.strategy.metrics['total_return'], 
                self.strategy.metrics['trades'], 
                self.strategy.metrics['winning_trades'], 
                self.strategy.metrics['losing_trades'], 
                self.strategy.metrics['max_drawdown'], 
                self.strategy.metrics['sharpe_ratio']
            ))
            
            conn.commit()
            cur.close()
            conn.close()

        except Exception as e:
            print(f"Error storing results in PostgreSQL: {e}")

# Function to fetch data from PostgreSQL
def fetch_data(symbol, fromdate, todate):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host='localhost'
        )
        cur = conn.cursor()

        query = f"SELECT date, open, high, low, close, volume FROM {symbol}_data WHERE date BETWEEN '{fromdate}' AND '{todate}' ORDER BY date"
        cur.execute(query)
        data = cur.fetchall()

        df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        df['date'] = pd.to_datetime(df['date'])  # Convert date column to datetime format
        df.set_index('date', inplace=True)

        cur.close()
        conn.close()

        return df

    except Exception as e:
        print(f"Error fetching data from PostgreSQL: {e}")
        return None

# Function to run backtest
def run_backtest(strategy_class, symbol, fromdate, todate, cash=10000.0, indicator_params=None):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy_class, **(indicator_params or {}))

    # Fetch data from PostgreSQL
    data = fetch_data(symbol, fromdate, todate)
    if data is None or data.empty:
        print(f"No data available for {symbol} between {fromdate} and {todate}")
        return

    # Create a Data Feed
    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)
    cerebro.broker.setcash(cash)

    cerebro.addanalyzer(MetricsAnalyzer, _name='metrics')

    print(f"Running backtest for {strategy_class.__name__} on {symbol.upper()}")
    print(f"Data Range: {fromdate} to {todate}")

    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    results = cerebro.run()
    metrics_analyzer = results[0].analyzers.metrics

    print(f"Ending Portfolio Value: {cerebro.broker.getvalue():.2f}")
    print(f"Total Return: {metrics_analyzer.strategy.metrics['total_return']:.2f}%")
    print(f"Number of Trades: {metrics_analyzer.strategy.metrics['trades']}")
    print(f"Winning Trades: {metrics_analyzer.strategy.metrics['winning_trades']}")
    print(f"Losing Trades: {metrics_analyzer.strategy.metrics['losing_trades']}")
    print(f"Max Drawdown: {metrics_analyzer.strategy.metrics['max_drawdown']:.2f}%")
    print(f"Sharpe Ratio: {metrics_analyzer.strategy.metrics['sharpe_ratio']:.2f}\n")

    return metrics_analyzer.strategy.metrics

# Load configuration from JSON file
with open('/home/moraa/Documents/10_academy/Week-9/Crypto-Trading-Engineering/MLOps/backend/src/run_backtest/backtest_config.json', 'r') as f:
    config = json.load(f)

# Run backtests for all strategies defined in the configuration
for strategy_conf in config['strategies']:
    strategy_name = strategy_conf['name']
    params = strategy_conf.get('params', {})
    
    # Resolve strategy class by name
    if strategy_name == 'SMAStrategy':
        strategy_class = bt.Strategy
    elif strategy_name == 'EMAStrategy':
        strategy_class = bt.Strategy
    elif strategy_name == 'RSIStrategy':
        strategy_class = bt.Strategy
    elif strategy_name == 'BollingerBandsStrategy':
        strategy_class = bt.Strategy
    elif strategy_name == 'AroonOscillatorStrategy':
        strategy_class = bt.Strategy
    elif strategy_name == 'StochasticOscillatorStrategy':
        strategy_class = bt.Strategy
    else:
        print(f"Unknown strategy: {strategy_name}. Skipping...")
        continue

    symbol = 'btc'  # Adjust this based on your strategy and data
    fromdate = datetime.datetime.strptime(config['fromdate'], '%Y-%m-%d')
    todate = datetime.datetime.strptime(config['todate'], '%Y-%m-%d')
    cash = config['cash']

    metrics = run_backtest(strategy_class, symbol, fromdate, todate, cash, params)



