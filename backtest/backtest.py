from itertools import product
import datetime
import json
import backtrader as bt

# Define strategies
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
    params = (('rsi_period', 14),)
    
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
    
    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy()
        else:
            if self.rsi > 70:
                self.sell()


class BollingerBandsStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2.0))
    def __init__(self):
        self.bbands = bt.indicators.BollingerBands(period=self.params.period, devfactor=self.params.devfactor)
    def next(self):
        if not self.position:
            if self.data.close[0] < self.bbands.bot[0]:
                self.buy()
        else:
            if self.data.close[0] > self.bbands.top[0]:
                self.sell()

class AroonOscillatorStrategy(bt.Strategy):
    params = (('period', 25),)
    def __init__(self):
        self.aroon = bt.indicators.AroonOscillator(self.data, period=self.params.period)
    def next(self):
        if not self.position:
            if self.aroon[0] > 0:
                self.buy()
        else:
            if self.aroon[0] < 0:
                self.sell()

class StochasticOscillatorStrategy(bt.Strategy):
    params = (('percK', 14), ('percD', 3))
    def __init__(self):
        self.stoch = bt.indicators.Stochastic(self.data, period=self.params.percK, period_dfast=self.params.percD)
    def next(self):
        if not self.position:
            if self.stoch.percK[0] < 20:
                self.buy()
        else:
            if self.stoch.percK[0] > 80:
                self.sell()

# Metrics Analyzer
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


        
def run_backtest(strategy_class, strategy_params, data_path, fromdate, todate, cash=10000.0):
    cerebro = bt.Cerebro()

    # Add the strategy class with its parameters
    cerebro.addstrategy(strategy_class, **strategy_params)

    # Load data from CSV file
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

    print(f"Running backtest for {strategy_class.__name__} with params {strategy_params}")
    
    try:
        result = cerebro.run()
    except Exception as e:
        print(f"Exception during backtesting: {e}")
        return
    
    # Retrieve metrics from MetricsAnalyzer
    metrics = result[0].analyzers.metrics

    # Print and display results
    print(f"Starting Portfolio Value: {cash}")
    print(f"Ending Portfolio Value: {cerebro.broker.getvalue():.2f}")
    print(f"Total Return: {metrics.total_return:.2f}%")
    print(f"Number of Trades: {metrics.trades}")
    print(f"Winning Trades: {metrics.winning_trades}")
    print(f"Losing Trades: {metrics.losing_trades}")
    print(f"Max Drawdown: {metrics.max_drawdown:.2f}%")
    print(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")

    # Plot the strategy
    try:
        cerebro.plot(style='candle', volume=False, barup='lightgreen', bardown='red')
    except bt.errors.BTError as e:
        print(f"An error occurred while plotting: {e}")

if __name__ == "__main__":
    with open('backtest_config.json', 'r') as f:
        config = json.load(f)

    data_path = config['data_path']
    cash = config['cash']

    for date_range in config['date_ranges']:
        fromdate = datetime.datetime.strptime(date_range['fromdate'], '%Y-%m-%d')
        todate = datetime.datetime.strptime(date_range['todate'], '%Y-%m-%d')

        for strategy_conf in config['strategies']:
            strategy_name = strategy_conf['name']
            params = strategy_conf.get('params', {})
            strategy_class = globals().get(strategy_name)

            if not strategy_class:
                print(f"Strategy {strategy_name} not found.")
                continue

            # Generate all possible combinations of parameters
            try:
                param_combinations = list(product(*[params[key]['range'] for key in params])) or [()]
            except KeyError as e:
                print(f"Missing 'range' for parameter {e} in strategy {strategy_name}")
                continue

            for param_set in param_combinations:
                strategy_params = {key: value for key, value in zip(params.keys(), param_set)}
                print(f"\nTesting {strategy_name} with params: {strategy_params}")
                run_backtest(strategy_class, strategy_params, data_path, fromdate, todate, cash)
