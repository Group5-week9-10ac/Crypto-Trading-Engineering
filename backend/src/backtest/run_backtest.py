import sys
import json
import datetime
import backtrader as bt
import math

# Import the strategies and MetricsAnalyzer from backtest.py
from backtest import SMAStrategy, EMAStrategy, RSIStrategy, BollingerBandsStrategy, AroonOscillatorStrategy, StochasticOscillatorStrategy, MetricsAnalyzer

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

    results = {
        'total_return': metrics.strategy.metrics['total_return'],
        'trades': metrics.strategy.metrics['trades'],
        'winning_trades': metrics.strategy.metrics['winning_trades'],
        'losing_trades': metrics.strategy.metrics['losing_trades'],
        'max_drawdown': metrics.strategy.metrics['max_drawdown'],
        'sharpe_ratio': metrics.strategy.metrics['sharpe_ratio']
    }

    return results

if __name__ == "__main__":
    # Load configuration from command-line argument
    config = json.loads(sys.argv[1])

    strategy_name = config['strategy']
    data_path = config['data_path']
    fromdate = datetime.datetime.strptime(config['fromdate'], '%Y-%m-%d')
    todate = datetime.datetime.strptime(config['todate'], '%Y-%m-%d')
    cash = config['cash']
    params = config.get('params', {})

    strategy = globals()[strategy_name]

    # Run the backtest
    results = run_backtest(strategy, data_path, fromdate, todate, cash, params)
    
    # Output results as JSON
    print(json.dumps(results))

