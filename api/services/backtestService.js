const { Pool } = require('pg');
const pool = new Pool();

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

async function runBacktest(strategyName, symbol, fromDate, toDate, cash) {
    // Function implementation here
}

// Export the functions
module.exports = {
    checkBacktestExists,
    runBacktest
};
