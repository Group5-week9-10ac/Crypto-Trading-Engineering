
CREATE DATABASE IF NOT EXISTS Crypto_trading;

CREATE TABLE cryptocurrencies (
    crypto_id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL 
);

CREATE TABLE strategies (
    strategy_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE historical_data (
    crypto_name VARCHAR(10) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    high FLOAT NOT NULL,
    low FLOAT NOT NULL,
    close FLOAT NOT NULL,
    adj_close FLOAT NOT NULL,
    volume BIGINT NOT NULL,
    PRIMARY KEY (symbol, date),
    FOREIGN KEY (symbol) REFERENCES cryptocurrencies(symbol)
);

CREATE TABLE backtests (
    backtest_id SERIAL PRIMARY KEY,
    crypto_id INT NOT NULL,
    strategy_id INT NOT NULL,
    parameter_set JSONB NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    cash FLOAT NOT NULL,
    FOREIGN KEY (crypto_id) REFERENCES cryptocurrencies(crypto_id),
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id)
);

CREATE TABLE results (
    result_id SERIAL PRIMARY KEY,
    backtest_id INT NOT NULL,
    total_return FLOAT NOT NULL,
    trades INT NOT NULL,
    winning_trades INT NOT NULL,
    losing_trades INT NOT NULL,
    max_drawdown FLOAT NOT NULL,
    sharpe_ratio FLOAT NOT NULL,
    ending_portfolio_value FLOAT NOT NULL,
    FOREIGN KEY (backtest_id) REFERENCES backtests(backtest_id)
);
