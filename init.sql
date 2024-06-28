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
