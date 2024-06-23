const backtestService = require('../services/backtestService');

exports.runBacktest = async (req, res) => {
  try {
    const { strategyName, symbol, fromDate, toDate, cash } = req.body;
    const result = await backtestService.runBacktest(strategyName, symbol, fromDate, toDate, cash);
    res.status(200).json(result);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
};
