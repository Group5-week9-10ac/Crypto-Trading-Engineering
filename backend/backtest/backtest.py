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
import logging
from typing import Dict, Optional, Type

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_exceptions(func):
    """
    Decorator to log exceptions for functions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Exception occurred in {func.__name__}: {e}")
            raise
    return wrapper

class SMAStrategy(bt.Strategy):
    """
    Strategy using Simple Moving Average (SMA).
    """
    params = (('period', 15),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.sell()

class EMAStrategy(bt.Strategy):
    """
    Strategy using Exponential Moving Average (EMA).
    """
    params = (('period', 20),)

    def __init__(self):
        self.ema = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:
            if self.data.close[0] > self.ema[0]:
                self.buy()
        elif self.data.close[0] < self.ema[0]:
            self.sell()

class RSIStrategy(bt.Strategy):
    """
    Strategy using Relative Strength Index (RSI).
    """
    params = (('period', 14), ('overbought', 70), ('oversold', 30))

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.period)

    def next(self):
        if not self.position:
            if self.rsi < self.params.oversold:
                self.buy()
        elif self.rsi > self.params.overbought:
            self.sell()

class BollingerBandsStrategy(bt.Strategy):
    """
    Strategy using Bollinger Bands.
    """
    params = (('period', 20), ('devfactor', 2))

    def __init__(self):
        self.bbands = bt.indicators.BollingerBands(period=self.params.period, devfactor=self.params.devfactor)

    def next(self):
        if not self.position:
            if self.data.close[0] < self.bbands.lines.bot:
                self.buy()
        elif self.data.close[0] > self.bbands.lines.top:
            self.sell()

class AroonOscillatorStrategy(bt.Strategy):
    """
    Strategy using Aroon Oscillator.
    """
    params = (('period', 14),)

    def __init__(self):
        self.aroon = bt.indicators.Aroon(period=self.params.period)

    def next(self):
        if not self.position:
            if self.aroon.lines.up > self.aroon.lines.down:
                self.buy()
        elif self.aroon.lines.up < self.aroon.lines.down:
            self.sell()

class StochasticOscillatorStrategy(bt.Strategy):
    """
    Strategy using Stochastic Oscillator.
    """
    params = (('period', 14), ('overbought', 80), ('oversold', 20))

    def __init__(self):
        self.stochastic = bt.indicators.Stochastic(period=self.params.period)

    def next(self):
        if not self.position:
            if self.stochastic.lines.percK < self.params.oversold:
                self.buy()
        elif self.stochastic.lines.percK > self.params.overbought:
            self.sell()

class MetricsAnalyzer(bt.Analyzer):
    """
    Analyzer class for calculating and storing backtest metrics.
    """
    def start(self):
        self.returns = []
        self.trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.drawdown = 0
        self.max_drawdown = 0
        self.sharpe_ratio = 0

    def notify_trade(self, trade: bt.Trade) -> None:
        if trade.isclosed:
            self.trades += 1
            if trade.pnl > 0:
                self.winning_trades += 1
            else:
                self.losing_trades += 1

    def next(self) -> None:
        portfolio_value = self.strategy.broker.getvalue()
        self.returns.append(portfolio_value)

    def stop(self) -> None:
        initial_value = self.returns[0] if self.returns else 0
        final_value = self.returns[-1] if self.returns else 0
        total_return = (final_value - initial_value) / initial_value if initial_value else 0

        if len(self.returns) > 1:
            avg_return = sum(self.returns) / len(self.returns)
            stddev = math.sqrt(sum((r - avg_return) ** 2 for r in self.returns) / len(self.returns))
            self.sharpe_ratio = avg_return / stddev if stddev else 0

        peak = self.returns[0]
        for value in self.returns:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak if peak else 0
            if drawdown > self.max_drawdown:
                self.max_drawdown = drawdown

        self.strategy.metrics = {
            'total_return': total_return * 100,
            'trades': self.trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'max_drawdown': self.max_drawdown * 100,
            'sharpe_ratio': self.sharpe_ratio
        }

        self._store_results()

    @log_exceptions
    def _store_results(self) -> None:
        """
        Store metrics in PostgreSQL.
        """
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

        except psycopg2.Error as e:
            logging.error(f"Database error: {e}")

@log_exceptions
def fetch_data(symbol: str, fromdate: str, todate: str) -> Optional[pd.DataFrame]:
    """
    Fetch historical trading data from PostgreSQL database.

    :param symbol: The symbol of the asset.
    :param fromdate: The start date of the data.
    :param todate: The end date of the data.
    :return: DataFrame containing the fetched data, or None if an error occurs.
    """
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
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        cur.close()
        conn.close()

        return df

    except psycopg2.Error as e:
        logging.error(f"Error fetching data from PostgreSQL: {e}")
        return None

@log_exceptions
def save_results_to_json(metrics: Dict[str, float], filename: str = 'backtest_results.json') -> None:
    """
    Save the backtest results to a JSON file.

    :param metrics: Dictionary containing the metrics to be saved.
    :param filename: The filename where the results will be saved.
    """
    with open(filename, 'w') as f:
        json.dump(metrics, f)

@log_exceptions
def run_backtest(strategy_name: str, from_date: str, to_date: str, cash: float = 10000.0, params: Optional[Dict[str, float]] = None) -> Optional[Dict[str, float]]:
    """
    Run the backtest for a given strategy and log the results with MLflow.

    :param strategy_name: The name of the strategy to test.
    :param from_date: The start date for the backtest.
    :param to_date: The end date for the backtest.
    :param cash: The initial cash for the backtest.
    :param params: Optional parameters for the strategy.
    :return: Dictionary of metrics if successful, None if failed.
    """
    try:
        mlflow.set_experiment("Backtest_Experiments")
        mlflow.start_run()

        mlflow.log_param('strategy_name', strategy_name)
        mlflow.log_param('from_date', from_date)
        mlflow.log_param('to_date', to_date)
        mlflow.log_param('initial_cash', cash)
        if params:
            for key, value in params.items():
                mlflow.log_param(key, value)

        cerebro = bt.Cerebro()
        
        strategies: Dict[str, Type[bt.Strategy]] = {
            'SMAStrategy': SMAStrategy,
            'EMAStrategy': EMAStrategy,
            'RSIStrategy': RSIStrategy,
            'BollingerBandsStrategy': BollingerBandsStrategy,
            'AroonOscillatorStrategy': AroonOscillatorStrategy,
            'StochasticOscillatorStrategy': StochasticOscillatorStrategy
        }

        if strategy_name not in strategies:
            raise ValueError(f"Strategy '{strategy_name}' is not implemented.")

        cerebro.addstrategy(strategies[strategy_name], **(params or {}))

        data = fetch_data('btc', from_date, to_date)
        if data is None or data.empty:
            raise ValueError(f"No data available for 'btc' between {from_date} and {to_date}")

        data_feed = bt.feeds.PandasData(dataname=data)
        cerebro.adddata(data_feed)
        cerebro.broker.setcash(cash)
        cerebro.addanalyzer(MetricsAnalyzer, _name='metrics')

        logging.info(f"Running backtest for {strategy_name} on 'btc'")
        logging.info(f"Data Range: {from_date} to {to_date}")
        logging.info(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")

        results = cerebro.run()
        if not results:
            raise RuntimeError("Backtesting returned None, check input parameters and data availability")

        metrics_analyzer = results[0].analyzers.metrics
        metrics = metrics_analyzer.strategy.metrics
        mlflow.log_metric('ending_portfolio_value', cerebro.broker.getvalue())
        mlflow.log_metric('total_return', metrics['total_return'])
        mlflow.log_metric('number_of_trades', metrics['trades'])
        mlflow.log_metric('winning_trades', metrics['winning_trades'])
        mlflow.log_metric('losing_trades', metrics['losing_trades'])
        mlflow.log_metric('max_drawdown', metrics['max_drawdown'])
        mlflow.log_metric('sharpe_ratio', metrics['sharpe_ratio'])

        artifact_path = '/home/moraa/Documents/10_academy/Week-9/Crypto-Trading-Engineering/MLOps/artifact'
        if os.path.exists(artifact_path):
            for filename in os.listdir(artifact_path):
                file_path = os.path.join(artifact_path, filename)
                mlflow.log_artifact(file_path)

        save_results_to_json(metrics)

        logging.info(f"Ending Portfolio Value: {cerebro.broker.getvalue():.2f}")
        logging.info(f"Total Return: {metrics['total_return']:.2f}%")
        logging.info(f"Number of Trades: {metrics['trades']}")
        logging.info(f"Winning Trades: {metrics['winning_trades']}")
        logging.info(f"Losing Trades: {metrics['losing_trades']}")
        logging.info(f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
        logging.info(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")

        mlflow.end_run()

        return metrics

    except Exception as e:
        logging.error(f"Error running backtest: {str(e)}")
        mlflow.end_run(status='FAILED')
        return None
