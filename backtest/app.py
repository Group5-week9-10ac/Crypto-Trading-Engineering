from flask import Flask, render_template, request
import datetime
from backtest import run_backtest, SMAStrategy, EMAStrategy, RSIStrategy, BollingerBandsStrategy, AroonOscillatorStrategy, StochasticOscillatorStrategy

app = Flask(__name__)

# Add strategies to globals() so they can be accessed dynamically
strategy_map = {
    1: 'SMAStrategy',
    2: 'EMAStrategy',
    3: 'RSIStrategy',
    4: 'BollingerBandsStrategy',
    5: 'AroonOscillatorStrategy',
    6: 'StochasticOscillatorStrategy'
}

# Add all strategy classes to globals() for dynamic access
globals().update({
    'SMAStrategy': SMAStrategy,
    'EMAStrategy': EMAStrategy,
    'RSIStrategy': RSIStrategy,
    'BollingerBandsStrategy': BollingerBandsStrategy,
    'AroonOscillatorStrategy': AroonOscillatorStrategy,
    'StochasticOscillatorStrategy': StochasticOscillatorStrategy
})

# Mapping of cryptocurrency IDs to their respective data file paths
crypto_file_paths = {
    9: '../data/BTC-USD.csv',
    10: '../data/ETH-USD.csv',
    12: '../data/USDT-USD.csv',
    13: '../data/BNB-USD.csv',
    11: '../data/SOL-USD.csv'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    cash = float(request.form['cash'])
    fromdate = datetime.datetime.strptime(request.form['fromdate'], '%Y-%m-%d')
    todate = datetime.datetime.strptime(request.form['todate'], '%Y-%m-%d')
    crypto_id = int(request.form['crypto_id'])  # Get the selected crypto ID
    strategy_id = int(request.form['strategy_id'])
    strategy_name = strategy_map.get(strategy_id)

    # Get the data file path based on selected cryptocurrency
    if crypto_id in crypto_file_paths:
        file_path = crypto_file_paths[crypto_id]
    else:
        return "Invalid cryptocurrency ID"

    # Initialize strategy_params with default values
    strategy_params = {}

    if strategy_id == 1:  # SMAStrategy
        strategy_params = {
            'period': int(request.form.get('period', 15)),
            'stop_loss': float(request.form.get('stop_loss', 0.02))
        }
    elif strategy_id == 2:  # EMAStrategy
        strategy_params = {
            'period': int(request.form.get('ema_period', 15))
        }
    elif strategy_id == 3:  # RSIStrategy
        strategy_params = {
            'period': int(request.form.get('rsi_period', 14)),
            'stop_loss': float(request.form.get('stop_loss', 0.02))
        }
    elif strategy_id == 4:  # BollingerBandsStrategy
        strategy_params = {
            'period': int(request.form.get('bb_period', 20)),
            'devfactor': float(request.form.get('devfactor', 2.0))
        }
    elif strategy_id == 5:  # AroonOscillatorStrategy
        strategy_params = {
            'period': int(request.form.get('aroon_period', 25))
        }
    elif strategy_id == 6:  # StochasticOscillatorStrategy
        strategy_params = {
            'percK': int(request.form.get('percK', 14)),
            'percD': int(request.form.get('percD', 3))
        }
    # Add more strategies here as needed

    try:
        # Run the backtest
        strategy_class = globals().get(strategy_name)
        if strategy_class:
            result = run_backtest(
                strategy_class=strategy_class,  # Dynamically get the strategy class
                strategy_params=strategy_params,
                data_path=file_path,
                fromdate=fromdate,
                todate=todate,
                cash=cash,
                crypto_id=crypto_id,
                strategy_id=strategy_id
            )

            # Render the result using a template
            return render_template('result.html', result=result)
        else:
            return f"Strategy {strategy_name} not found"
    except Exception as e:
        return f"An error occurred during backtesting: {e}"


if __name__ == '__main__':
    app.run(debug=True)
