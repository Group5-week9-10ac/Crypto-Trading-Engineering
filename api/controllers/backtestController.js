const { checkBacktestExists } = require('../services/backtestService');
const sendBacktestRequest = require('../kafka/producer');

async function handleBacktestRequest(req, res) {
    const strategyName = req.body.strategyName;
    const symbol = req.body.symbol;
    const fromDate = req.body.fromDate;
    const toDate = req.body.toDate;
    const cash = req.body.cash;

    try {
        const backtestExists = await checkBacktestExists(strategyName, symbol, fromDate, toDate);

        if (backtestExists) {
            res.status(400).json({ message: 'Backtest results already exist for this range.' });
        } else {
            const backtestRequest = { strategyName, symbol, fromDate, toDate, cash };
            await sendBacktestRequest(backtestRequest);
            res.status(200).json({ message: 'Backtest request sent successfully.' });
        }
    } catch (error) {
        console.error('Error handling backtest request:', error);
        res.status(500).json({ message: 'Error handling backtest request.', error: error.message });
    }
}

module.exports = {
    handleBacktestRequest
};
