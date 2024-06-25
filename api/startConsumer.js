const express = require('express');
const { startConsumer } = require('./kafka/consumer');

const app = express();
const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);

  startConsumer().then(() => {
    console.log('Kafka consumer started successfully');
  }).catch(err => {
    console.error('Error starting Kafka consumer', err);
  });
});


