const pool = require('../config/database');
const { exec } = require('child_process');

exports.runBacktest = (strategyName, symbol, fromDate, toDate, cash) => {
  return new Promise((resolve, reject) => {
    // Prepare command to run Python backtest script
    const command = `python3 /home/moraa/Documents/10_academy/Week-9/Crypto-Trading-Engineering/MLOps/backend/src/run_backtest/backtest.py ${strategyName} ${symbol} ${fromDate} ${toDate} ${cash}`;
    
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing command: ${error}`);
        return reject(error);
      }
      
      // Parse and return the result
      try {
        const result = JSON.parse(stdout);
        resolve(result);
      } catch (parseError) {
        console.error(`Error parsing result: ${parseError}`);
        reject(parseError);
      }
    });
  });
};
