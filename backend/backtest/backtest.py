import backtrader as bt
import datetime
import json
import math
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
import mlflow
import mlflow.sklearn

# Load environment variables from .env file
load_dotenv()

# Define your strategy classes (unchanged)

class SMAStrategy(bt.Strategy):
    params = (('period', 15),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:  # not in the market
            if self.data.close[0] > self.sma[0]:
                self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.sell()

class EMAStrategy(bt.Strategy):
    params = (('period', 15),)

    def __init__(self):
        self.ema = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:  # not in the market
            if self.data.close[0] > self.ema[0]:
                self.buy()
        elif self.data.close[0] < self.ema[0]:
            self.sell()

class RSIStrategy(bt.Strategy):
    params = (('period', 14),)

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy()
        elif self.rsi > 70:
            self.sell()

class BollingerBandsStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2.0),)

    def __init__(self):
        self.bbands = bt.indicators.BollingerBands(self.data.close, period=self.params.period, devfactor=self.params.devfactor)

    def next(self):
        if not self.position:
            if self.data.close[0] < self.bbands.lines.bot[0]:
                self.buy()
        elif self.data.close[0] > self.bbands.lines.top[0]:
            self.sell()

class AroonOscillatorStrategy(bt.Strategy):
    params = (('period', 14),)

    def __init__(self):
        self.aroon = bt.indicators.AroonOscillator(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:
            if self.aroon > 50:
                self.buy()
        elif self.aroon < -50:
            self.sell()

class StochasticOscillatorStrategy(bt.Strategy):
    params = (('period', 14), ('percK', 3), ('percD', 3),)

    def __init__(self):
        self.stoch = bt.indicators.Stochastic(self.data, period=self.params.period, period_dfast=self.params.percK, period_dslow=self.params.percD)

    def next(self):
        if not self.position:
            if self.stoch.percK < 20:
                self.buy()
        elif self.stoch.percK > 80:
            self.sell()

# Metrics analyzer class (unchanged)

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

        # Insert results into PostgreSQL (unchanged)

        try:
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host='localhost'
            )
            cur = conn.cursor()

            query = """
            INSERT INTO backtest_results (strategy_name, from_date, to_date, total_return, trades, winning_trades, losing_trades, max_drawdown, sharpe_ratio)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (
                self.strategy.__class__.__name__, 
                self.strategy.params.from_date, 
                self.strategy.params.to_date, 
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

# Function to fetch data from PostgreSQL (unchanged)

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
def run_backtest(strategy_name, from_date, to_date, cash=10000.0, params=None):
    try:
        # Initialize MLflow
        mlflow.set_experiment("Backtest_Experiments")  # Set the experiment name
        mlflow.start_run()

        # Log parameters
        mlflow.log_param('strategy_name', strategy_name)
        mlflow.log_param('from_date', from_date)
        mlflow.log_param('to_date', to_date)
        mlflow.log_param('initial_cash', cash)
        if params:
            for key, value in params.items():
                mlflow.log_param(key, value)

        # Initialize Cerebro engine
        cerebro = bt.Cerebro()
        
        # Strategy dictionary
        strategies = {
            'SMAStrategy': SMAStrategy,
            'EMAStrategy': EMAStrategy,
            'RSIStrategy': RSIStrategy,
            'BollingerBandsStrategy': BollingerBandsStrategy,
            'AroonOscillatorStrategy': AroonOscillatorStrategy,
            'StochasticOscillatorStrategy': StochasticOscillatorStrategy
        }

        # Check if strategy exists
        if strategy_name not in strategies:
            raise ValueError(f"Strategy '{strategy_name}' is not implemented.")

        # Add strategy to Cerebro
        cerebro.addstrategy(strategies[strategy_name], **(params or {}))

        # Fetch data
        data = fetch_data('btc', from_date, to_date)
        if data is None or data.empty:
            raise ValueError(f"No data available for 'btc' between {from_date} and {to_date}")

        # Add data feed to Cerebro
        data_feed = bt.feeds.PandasData(dataname=data)
        cerebro.adddata(data_feed)
        cerebro.broker.setcash(cash)
        cerebro.addanalyzer(MetricsAnalyzer, _name='metrics')

        # Print initial state
        print(f"Running backtest for {strategy_name} on 'btc'")
        print(f"Data Range: {from_date} to {to_date}")
        print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")

        # Run backtest
        results = cerebro.run()
        if not results:
            raise RuntimeError("Backtesting returned None, check input parameters and data availability")

        metrics_analyzer = results[0].analyzers.metrics

        # Log metrics
        metrics = metrics_analyzer.strategy.metrics
        mlflow.log_metric('ending_portfolio_value', cerebro.broker.getvalue())
        mlflow.log_metric('total_return', metrics['total_return'])
        mlflow.log_metric('number_of_trades', metrics['trades'])
        mlflow.log_metric('winning_trades', metrics['winning_trades'])
        mlflow.log_metric('losing_trades', metrics['losing_trades'])
        mlflow.log_metric('max_drawdown', metrics['max_drawdown'])
        mlflow.log_metric('sharpe_ratio', metrics['sharpe_ratio'])

        # Log additional artifacts (e.g., plot of the strategy or any other relevant file)
        artifact_path = '/home/moraa/Documents/10_academy/Week-9/Crypto-Trading-Engineering/MLOps/artifact'
        if os.path.exists(artifact_path):
            for filename in os.listdir(artifact_path):
                file_path = os.path.join(artifact_path, filename)
                mlflow.log_artifact(file_path)

        # Print results
        print(f"Ending Portfolio Value: {cerebro.broker.getvalue():.2f}")
        print(f"Total Return: {metrics['total_return']:.2f}%")
        print(f"Number of Trades: {metrics['trades']}")
        print(f"Winning Trades: {metrics['winning_trades']}")
        print(f"Losing Trades: {metrics['losing_trades']}")
        print(f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
        print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")

        # End MLflow run
        mlflow.end_run()

        return metrics
    except Exception as e:
        print(f"Error running backtest: {str(e)}")
        mlflow.end_run(status='FAILED')
        return None
