CREATE TABLE IF NOT EXISTS btc_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    adjclose REAL NOT NULL,
    volume REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS bnb_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    adjclose REAL NOT NULL,
    volume REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS eth_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    adjclose REAL NOT NULL,
    volume REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS sol_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    adjclose REAL NOT NULL,
    volume REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS xrp_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    adjclose REAL NOT NULL,
    volume REAL NOT NULL
);