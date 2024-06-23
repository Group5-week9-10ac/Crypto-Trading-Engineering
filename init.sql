-- Create BTC table
CREATE TABLE IF NOT EXISTS btc_data (
    date TIMESTAMP WITH TIME ZONE PRIMARY KEY,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    dividends NUMERIC,
    stock_splits NUMERIC
);

-- Create ETH table
CREATE TABLE IF NOT EXISTS eth_data (
    date TIMESTAMP WITH TIME ZONE PRIMARY KEY,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    dividends NUMERIC,
    stock_splits NUMERIC
);

CREATE TABLE IF NOT EXISTS backtest_results (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(255),
    symbol VARCHAR(10),
    from_date DATE,
    to_date DATE,
    total_return FLOAT,
    trades INTEGER,
    winning_trades INTEGER,
    losing_trades INTEGER,
    max_drawdown FLOAT,
    sharpe_ratio FLOAT
);
