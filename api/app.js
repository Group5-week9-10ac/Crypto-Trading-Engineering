const express = require('express');
const { startConsumer, stopConsumer } = require('./kafka/consumer');

const app = express();
const port = process.env.PORT || 4000;

app.get('/', (req, res) => res.send('Kafka Consumer is running'));

const server = app.listen(port, async () => {
  console.log(`Server is running on port ${port}`);
  await startConsumer();
});

const shutdown = async () => {
  console.log('Shutting down server...');
  await stopConsumer();
  server.close(() => {
    console.log('Express server closed');
    process.exit(0);
  });
};

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
