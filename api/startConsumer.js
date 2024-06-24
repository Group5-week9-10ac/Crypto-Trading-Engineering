const express = require('express');
const { startConsumer } = require('./kafka/consumer'); // Corrected path

const app = express();
const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);

  // Start the Kafka consumer
  startConsumer().then(() => {
    console.log('Kafka consumer started successfully');
  }).catch(err => {
    console.error('Error starting Kafka consumer', err);
  });
});

