const express = require('express');
const router = express.Router();
const backtestController = require('../controllers/backtestController');

// Define POST route for running backtest
router.post('/backtest', backtestController.handleBacktestRequest);

module.exports = router;
