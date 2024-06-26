var express = require('express');
var router = express.Router();
var { Pool } = require('pg');
var { spawn } = require('child_process');

const pool = new Pool({
    user: process.env.POSTGRES_USER,
    host: process.env.POSTGRES_HOST,
    database: process.env.POSTGRES_DB,
    password: process.env.POSTGRES_PASSWORD,
    port: 5432,
});

// Route to handle backtests
router.post('/', function(req, res, next) {
    const { strategyName, fromDate, toDate, initialCash, params } = req.body;

    // Convert params object to JSON string
    const paramsJson = JSON.stringify(params);

    // Spawn a Python process to run the backtest
    const pythonProcess = spawn('python3', ['path/to/your/backtest.py', strategyName, fromDate, toDate, initialCash, paramsJson]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            res.status(200).send('Backtest completed successfully');
        } else {
            res.status(500).send('Error running backtest');
        }
    });
});

module.exports = router;
