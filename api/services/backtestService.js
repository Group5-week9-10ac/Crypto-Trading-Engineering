const { Pool } = require('pg');
const pool = new Pool();
const { spawn } = require('child_process');
const path = require('path');

async function checkBacktestExists(strategyName, symbol, fromDate, toDate) {
    const query = `
        SELECT 1
        FROM backtest_results
        WHERE strategy_name = $1 AND symbol = $2 AND from_date = $3 AND to_date = $4
        LIMIT 1;
    `;
    const values = [strategyName, symbol, fromDate, toDate];

    try {
        const res = await pool.query(query, values);
        return res.rowCount > 0;
    } catch (err) {
        console.error('Error checking backtest existence:', err);
        throw err;
    }
}

async function getBacktestResults(strategyName, symbol, fromDate, toDate) {
    const query = `
        SELECT *
        FROM backtest_results
        WHERE strategy_name = $1 AND symbol = $2 AND from_date = $3 AND to_date = $4;
    `;
    const values = [strategyName, symbol, fromDate, toDate];

    try {
        const res = await pool.query(query, values);
        return res.rows;
    } catch (err) {
        console.error('Error fetching backtest results:', err);
        throw err;
    }
}

async function fetchHistoricalData(symbol, fromDate, toDate) {
    const query = `
        SELECT date, open, high, low, close, volume, adjclose
        FROM historical_data
        WHERE symbol = $1 AND date BETWEEN $2 AND $3
        ORDER BY date ASC;
    `;
    const values = [symbol, fromDate, toDate];

    try {
        const res = await pool.query(query, values);
        return res.rows;
    } catch (err) {
        console.error('Error fetching historical data:', err);
        throw err;
    }
}

async function runBacktest(strategyName, symbol, fromDate, toDate, cash) {
    const pythonScriptPath = path.join(__dirname, '../../backend/src/backtest/run_backtest.py');

    const historicalData = await fetchHistoricalData(symbol, fromDate, toDate);

    const backtestParams = {
        strategyName,
        symbol,
        fromDate,
        toDate,
        cash,
        data: historicalData,
    };

    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python3', [pythonScriptPath]);

        pythonProcess.stdin.write(JSON.stringify(backtestParams));
        pythonProcess.stdin.end();

        let result = '';
        pythonProcess.stdout.on('data', (data) => {
            result += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python error: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                return reject(new Error('Python script exited with code ' + code));
            }
            try {
                const backtestResult = JSON.parse(result);
                resolve(backtestResult);
            } catch (err) {
                reject(err);
            }
        });
    });
}

module.exports = {
    checkBacktestExists,
    getBacktestResults,
    runBacktest,
};
