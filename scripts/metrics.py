import backtrader as bt
import datetime
import os.path
import sys


def calculate_metrics(results, final_value, initial_cash):
    strat = results[0]
    
    cumulative_return = (final_value - initial_cash) / initial_cash
    returns = strat.analyzers.returns.get_analysis()
    sharpe = strat.analyzers.sharpe.get_analysis()
    drawdown = strat.analyzers.drawdown.get_analysis()
    
    best_return = max((val - initial_cash) / initial_cash for val in strat.broker.get_value_history())
    lowest_drawdown = drawdown.drawdown
    
    metrics = {
        "cumulative_return_manual": cumulative_return,
        "cumulative_return_analyzer": returns['rtot'],
        "sharpe_ratio": sharpe['sharperatio'],
        "max_drawdown": drawdown.drawdown,
        "best_return": best_return,
        "lowest_drawdown": lowest_drawdown
    }
    
    return metrics

def score_metrics(metrics):
    score = (
        metrics['cumulative_return_manual'] +
        metrics['sharpe_ratio'] -
        metrics['max_drawdown'] / 100
    )
    return score

def select_best_strategy(strategies, data_path, from_date, to_date, initial_cash):
    best_strategy = None
    best_score = float('-inf')
    best_metrics = None
    
    for strategy in strategies:
        results, final_value, initial_cash = run_backtest(strategy, data_path, from_date, to_date, initial_cash)
        metrics = calculate_metrics(results, final_value, initial_cash)
        score = score_metrics(metrics)
        
        if score > best_score:
            best_score = score
            best_strategy = strategy
            best_metrics = metrics
    
    return best_strategy, best_metrics