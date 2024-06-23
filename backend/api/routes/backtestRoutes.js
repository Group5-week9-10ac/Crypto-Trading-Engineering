const express = require('express');
const router = express.Router();
const backtestController = require('../controllers/backtestController');

router.post('/run-backtest', backtestController.runBacktest);

module.exports = router;
