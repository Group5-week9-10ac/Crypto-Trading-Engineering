const express = require('express');
const cors = require('cors');
const { startConsumer, stopConsumer } = require('./kafka/consumer');
const { connectProducer, disconnectProducer } = require('./kafka/producer');

const app = express();
const port = process.env.PORT || 4000;

// Middleware to handle JSON bodies
app.use(express.json());

// Use CORS middleware
const corsOptions = {
    origin: 'http://localhost:3000', // Ensure this matches the URL of your frontend
    methods: ['GET', 'POST'], // Add other HTTP methods if needed
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
};
app.use(cors(corsOptions));

// Handle preflight requests
app.options('*', cors(corsOptions));

app.get('/api', (req, res) => res.send('Kafka Consumer is running'));

// Signup route example
app.post('/auth/signup', async (req, res) => {
    try {
        // Your signup logic here...
        res.status(201).send('User signed up successfully');
    } catch (error) {
        res.status(500).send('Error signing up user');
    }
});

// Additional API routes here...

const server = app.listen(port, async () => {
    console.log(`Server is running on port ${port}`);
    await startConsumer();
    await connectProducer();
});

const shutdown = async () => {
    console.log('Shutting down server...');
    await stopConsumer();
    await disconnectProducer();
    server.close(() => {
        console.log('Express server closed');
        process.exit(0);
    });
};

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
