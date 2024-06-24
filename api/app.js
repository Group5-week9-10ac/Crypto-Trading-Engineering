const express = require('express');
const authRoutes = require('./routes/authRoutes');
const authMiddleware = require('./middleware/authMiddleware');
const startConsumer = require('./kafka/consumer');
require('dotenv').config();

const app = express();

// Middleware
app.use(express.json());

// Routes
app.use('/api/auth', authRoutes);

// Protected route example
app.get('/api/dashboard', authMiddleware, (req, res) => {
    res.json({ message: 'Welcome to the dashboard!' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
    startConsumer().then(() => {
        console.log('Kafka consumer started successfully');
    }).catch(err => {
        console.error('Error starting Kafka consumer:', err);
    });
});
