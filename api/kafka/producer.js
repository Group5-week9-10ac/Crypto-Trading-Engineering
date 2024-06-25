const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'backtest-producer',
  brokers: [process.env.KAFKA_BROKER || 'kafka:9092']
});

const producer = kafka.producer();

const connectProducer = async () => {
  await producer.connect();
  console.log('Connected to Kafka broker');
};

const sendBacktestRequest = async (message) => {
  try {
    await producer.send({
      topic: process.env.KAFKA_TOPIC || 'backtest-requests',
      messages: [{ value: JSON.stringify(message) }],
    });
    console.log('Message sent:', message);
  } catch (error) {
    console.error('Error sending message:', error);
  }
};

const disconnectProducer = async () => {
  try {
    await producer.disconnect();
    console.log('Kafka producer disconnected');
  } catch (error) {
    console.error('Error disconnecting Kafka producer:', error);
  }
};

module.exports = { connectProducer, sendBacktestRequest, disconnectProducer };
