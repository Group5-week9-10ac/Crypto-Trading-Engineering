const express = require('express');
const app = express();
const backtestRoutes = require('./routes/backtestRoutes');

// Middleware to parse JSON bodies
app.use(express.json());

// Use backtest routes
app.use('/api', backtestRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
