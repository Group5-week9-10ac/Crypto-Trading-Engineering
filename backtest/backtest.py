import datetime
import json
from itertools import product
import os
import backtrader as bt
import matplotlib.pyplot as plt
import psycopg2

# Database connection details
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_HOST='localhost'
DB_PORT='5433'
DB_NAME='crypto_trading'

class SMAStrategy(bt.Strategy):
    params = (('period', 15), ('stop_loss', 0.02))

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.period)
        self.atr = bt.indicators.ATR(self.data, period=14)

    def next(self):
        if len(self.data) < self.params.period:
            return
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                size = int(self.broker.cash / self.data.close[0])
                self.buy(size=size)
                self.stop_price = self.data.close[0] - self.atr[0] * self.params.stop_loss
        else:
            if self.data.close[0] < self.sma[0] or self.data.close[0] < self.stop_price:
                self.sell(size=self.position.size)


class EMAStrategy(bt.Strategy):
    params = (('period', 15), ('stop_loss', 0.02))

    def __init__(self):
        self.ema = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.params.period)
        self.atr = bt.indicators.ATR(self.data, period=14)

    def next(self):
        if len(self.data) < self.params.period:
            return
        if not self.position:
            if self.data.close[0] > self.ema[0]:
                size = int(self.broker.cash / self.data.close[0])
                self.buy(size=size)
                self.stop_price = self.data.close[0] - self.atr[0] * self.params.stop_loss
        else:
            if self.data.close[0] < self.ema[0] or self.data.close[0] < self.stop_price:
                self.sell(size=self.position.size)


class RSIStrategy(bt.Strategy):
    params = (
        ('period', 14),
        ('stop_loss', 0.02)  # Default stop loss value
    )

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.period)

    def next(self):
        if len(self.data) < self.params.period:
            return
        if not self.position:
            if self.rsi[0] < 30:
                self.buy()
                self.stop_price = self.data.close[0] * (1.0 - self.params.stop_loss)
        else:
            if self.rsi[0] > 70 or self.data.close[0] < self.stop_price:
                self.sell()


class BollingerBandsStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2.0), ('stop_loss', 0.02))

    def __init__(self):
        self.bbands = bt.indicators.BollingerBands(self.data.close, period=self.params.period, devfactor=self.params.devfactor)
        self.atr = bt.indicators.ATR(self.data, period=14)

    def next(self):
        if not self.position:
            if self.data.close[0] < self.bbands.lines.bot[0]:
                size = int(self.broker.cash / self.data.close[0])
                self.buy(size=size)
                self.stop_price = self.data.close[0] - self.atr[0] * self.params.stop_loss
        else:
            if self.data.close[0] > self.bbands.lines.top[0] or self.data.close[0] < self.stop_price:
                self.sell(size=self.position.size)


class AroonOscillatorStrategy(bt.Strategy):
    params = (('period', 25), ('stop_loss', 0.02))

    def __init__(self):
        self.aroon = bt.indicators.AroonOscillator(self.data, period=self.params.period)
        self.atr = bt.indicators.ATR(self.data, period=14)

    def next(self):
        if not self.position:
            if self.aroon[0] > 0:
                size = int(self.broker.cash / self.data.close[0])
                self.buy(size=size)
                self.stop_price = self.data.close[0] - self.atr[0] * self.params.stop_loss
        else:
            if self.aroon[0] < 0 or self.data.close[0] < self.stop_price:
                self.sell(size=self.position.size)


class StochasticOscillatorStrategy(bt.Strategy):
    params = (('percK', 14), ('percD', 3), ('stop_loss', 0.02))

    def __init__(self):
        self.stochastic = bt.indicators.Stochastic(self.data, period=self.params.percK, period_dfast=self.params.percD)
        self.atr = bt.indicators.ATR(self.data, period=14)

    def next(self):
        if not self.position:
            if self.stochastic.percK[0] > self.stochastic.percD[0]:
                size = int(self.broker.cash / self.data.close[0])
                self.buy(size=size)
                self.stop_price = self.data.close[0] - self.atr[0] * self.params.stop_loss
        else:
            if self.stochastic.percK[0] < self.stochastic.percD[0] or self.data.close[0] < self.stop_price:
                self.sell(size=self.position.size)


class MetricsAnalyzer(bt.Analyzer):
    def __init__(self):
        self.total_return = 0.0
        self.trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.max_drawdown = 0.0
        self.sharpe_ratio = 0.0

    def start(self):
        self.init_cash = self.strategy.broker.startingcash

    def stop(self):
        self.total_return = (self.strategy.broker.getvalue() / self.init_cash - 1.0) * 100

        # Handle strategies with TradeAnalyzer
        trade_analysis = self.strategy.analyzers.trade_analyzer.get_analysis()
        if trade_analysis:
            self.trades = trade_analysis.total.total
            self.winning_trades = trade_analysis.won.total
            self.losing_trades = trade_analysis.lost.total

        # Handle max drawdown
        drawdown_analysis = self.strategy.analyzers.drawdown.get_analysis()
        if drawdown_analysis:
            self.max_drawdown = drawdown_analysis['max']['drawdown']

        # Handle Sharpe ratio
        sharpe_ratio_analysis = self.strategy.analyzers.sharpe_ratio.get_analysis()
        if sharpe_ratio_analysis:
            self.sharpe_ratio = sharpe_ratio_analysis['sharperatio']


def insert_backtest(conn, crypto_id, strategy_id, parameter_set, start_date, end_date, cash):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO backtests (crypto_id, strategy_id, parameter_set, start_date, end_date, cash)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING backtest_id;
        """, (crypto_id, strategy_id, json.dumps(parameter_set), start_date, end_date, cash))
        return cur.fetchone()[0]


def insert_result(conn, backtest_id, total_return, trades, winning_trades, losing_trades, max_drawdown, sharpe_ratio, ending_portfolio_value):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO results (backtest_id, total_return, trades, winning_trades, losing_trades, max_drawdown, sharpe_ratio, ending_portfolio_value)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (backtest_id, total_return, trades, winning_trades, losing_trades, max_drawdown, sharpe_ratio, ending_portfolio_value))


# Function to run the backtest
def run_backtest(strategy_class, strategy_params, data_path, fromdate, todate, cash, crypto_id, strategy_id):
    try:
        cerebro = bt.Cerebro()
        cerebro.addstrategy(strategy_class, **strategy_params)  # Pass strategy_params as kwargs

        # Add data and set cash
        data = bt.feeds.GenericCSVData(
            dataname=data_path,
            nullvalue=0.0,
            dtformat=('%Y-%m-%d'),
            datetime=0,
            open=1,
            high=2,
            low=3,
            close=4,
            volume=5,
            adjclose=6,
            fromdate=fromdate,
            todate=todate
        )
        cerebro.adddata(data)
        cerebro.broker.setcash(cash)

        # Add analyzers
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
        cerebro.addanalyzer(MetricsAnalyzer, _name='metrics')

        # Run the strategy
        result = cerebro.run()
        metrics = result[0].analyzers.metrics  # Assuming only one strategy is added

        # Database insertion
        conn = psycopg2.connect(host='localhost', port='5433', dbname='crypto_trading', user='postgres', password='postgres')
        conn.autocommit = True

        # Insert backtest
        backtest_id = insert_backtest(conn, crypto_id, strategy_id, strategy_params, fromdate, todate, cash)

        # Insert results
        insert_result(conn, backtest_id, metrics.total_return, metrics.trades, metrics.winning_trades, metrics.losing_trades, metrics.max_drawdown, metrics.sharpe_ratio, cerebro.broker.getvalue())

        conn.close()

        # Return results for displaying in the web page
        return {
            "Starting Portfolio Value": cash,
            "Ending Portfolio Value": cerebro.broker.getvalue(),
            "Total Return": metrics.total_return,
            "Number of Trades": metrics.trades,
            "Winning Trades": metrics.winning_trades,
            "Losing Trades": metrics.losing_trades,
            "Max Drawdown": metrics.max_drawdown,
            "Sharpe Ratio": metrics.sharpe_ratio
        }

    except Exception as e:
        return f"An error occurred during backtesting: {e}"
