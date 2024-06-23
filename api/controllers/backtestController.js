const { runBacktest, checkBacktestExists } = require('../services/backtestService');

async function handleBacktestRequest(req, res) {
    // Example usage of runBacktest
    const strategyName = req.body.strategyName;
    const symbol = req.body.symbol;
    const fromDate = req.body.fromDate;
    const toDate = req.body.toDate;
    const cash = req.body.cash;

    try {
        const backtestExists = await checkBacktestExists(strategyName, symbol, fromDate, toDate);

        if (backtestExists) {
            // Handle case where backtest results already exist
            res.status(400).json({ message: 'Backtest results already exist for this range.' });
        } else {
            // Run the backtest
            const metrics = await runBacktest(strategyName, symbol, fromDate, toDate, cash);
            res.status(200).json({ message: 'Backtest completed successfully.', metrics });
        }
    } catch (error) {
        console.error('Error running backtest:', error);
        res.status(500).json({ message: 'Error running backtest.', error: error.message });
    }
}

module.exports = {
    handleBacktestRequest
};