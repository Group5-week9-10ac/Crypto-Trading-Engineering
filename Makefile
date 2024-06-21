PYTHON = python3
PYTHONPATH = /home/moraa/Documents/10_academy/Week-9/Crypto-Trading-Engineering/MLOps/

.PHONY: all load_data train_model analysis clean

all: load_data train_model analysis

load_data:
	@echo "=== Running data loading script ==="
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) backend/src/analysis/crypto_data/data_loader.py

train_model:
	@echo "=== Training LSTM model ==="
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) backend/src/analysis/time_series_forecasting/main.py

backtests:
	@echo "=== Running backtesting script ==="
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) backend/src/analysis/run_backtest.py

clean:
	@echo "=== Cleaning up ==="
	# Add commands to clean up here if needed




