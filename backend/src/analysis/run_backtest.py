import backtrader as bt
import datetime
import json
import math
import pandas as pd

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

        self.strategy.metrics = {
            'total_return': total_return * 100,
            'trades': self.trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'max_drawdown': self.max_drawdown * 100,
            'sharpe_ratio': self.sharpe_ratio
        }

# Define Strategies
class SMAStrategy(bt.Strategy):
    params = (('period', 15),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.period)

    def next(self):
        if len(self.data) < self.params.period:
            return
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                self.buy()
        else:
            if self.data.close[0] < self.sma[0]:
                self.sell()

class EMAStrategy(bt.Strategy):
    params = (('period', 15),)

    def __init__(self):
        self.ema = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.params.period)

    def next(self):
        if len(self.data) < self.params.period:
            return
        if not self.position:
            if self.data.close[0] > self.ema[0]:
                self.buy()
        else:
            if self.data.close[0] < self.ema[0]:
                self.sell()

class RSIStrategy(bt.Strategy):
    params = (('period', 14),)

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.period)

    def next(self):
        if len(self.data) < self.params.period:
            return
        if not self.position:
            if self.rsi[0] < 30:
                self.buy()
        else:
            if self.rsi[0] > 70:
                self.sell()

class BollingerBandsStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2.0),)

    def __init__(self):
        self.bbands = bt.indicators.BollingerBands(self.data.close, period=self.params.period, devfactor=self.params.devfactor)

    def next(self):
        if not self.position:
            if self.data.close[0] < self.bbands.lines.bot[0]:
                self.buy()
        else:
            if self.data.close[0] > self.bbands.lines.top[0]:
                self.sell()

class AroonOscillatorStrategy(bt.Strategy):
    params = (('period', 14),)

    def __init__(self):
        self.aroon = bt.indicators.AroonOscillator(period=self.params.period)

    def next(self):
        if not self.position:
            if self.aroon[0] > 0:
                self.buy()
        else:
            if self.aroon[0] < 0:
                self.sell()

class StochasticOscillatorStrategy(bt.Strategy):
    params = (('period', 14), ('percK', 3), ('percD', 3),)

    def __init__(self):
        self.stoch = bt.indicators.Stochastic(self.data, period=self.params.period, 
                                              period_dfast=self.params.percK, period_dslow=self.params.percD)

    def next(self):
        if not self.position:
            if self.stoch.lines.percK[0] < 20:
                self.buy()
        else:
            if self.stoch.lines.percK[0] > 80:
                self.sell()

def save_results_to_csv(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

def run_backtest(strategy, data_path, fromdate, todate, cash=10000.0, indicator_params=None):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy, **(indicator_params or {}))
    
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

    cerebro.addanalyzer(MetricsAnalyzer, _name='metrics')

    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    result = cerebro.run()
    metrics = result[0].analyzers.metrics

    print(f"Ending Portfolio Value: {cerebro.broker.getvalue():.2f}")
    print(f"Total Return: {metrics.strategy.metrics['total_return']:.2f}%")
    print(f"Number of Trades: {metrics.strategy.metrics['trades']}")
    print(f"Winning Trades: {metrics.strategy.metrics['winning_trades']}")
    print(f"Losing Trades: {metrics.strategy.metrics['losing_trades']}")
    print(f"Max Drawdown: {metrics.strategy.metrics['max_drawdown']:.2f}%")
    print(f"Sharpe Ratio: {metrics.strategy.metrics['sharpe_ratio']:.2f}\n")

    return metrics.strategy.metrics

# Load configuration
with open('backtest_config.json', 'r') as f:
    config = json.load(f)

data_path = config['data_path']
fromdate = datetime.datetime.strptime(config['fromdate'], '%Y-%m-%d')
todate = datetime.datetime.strptime(config['todate'], '%Y-%m-%d')
cash = config['cash']

# Run backtests for all strategies defined in the configuration
results = []
for strategy_conf in config['strategies']:
    strategy_name = strategy_conf['name']
    params = strategy_conf.get('params', {})
    strategy = globals()[strategy_name]
    
    print(f"Running backtest for {strategy_name}")
    metrics = run_backtest(strategy, data_path, fromdate, todate, cash, params)
    metrics['strategy'] = strategy_name
    results.append(metrics)

# Save results to CSV
save_results_to_csv(results, 'backtest_results.csv')
