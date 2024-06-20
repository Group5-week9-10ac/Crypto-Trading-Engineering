PYTHON = python3
PYTHONPATH = /home/moraa/Documents/10_academy/Week-9/Crypto-Trading-Engineering/MLOps/

.PHONY: all load_data clean

all: load_data

load_data:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) backend/src/backtest/crypto_data/data_loader.py

clean:
	rm -rf data/*.csv  # Remove all CSV files in data folder


