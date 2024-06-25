const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: [process.env.KAFKA_BROKER || 'kafka:9092']
});

const consumer = kafka.consumer({ groupId: 'test-group' });

const processMessage = async (message) => {
  // Your backtest processing logic here
  console.log('Processing message:', message);
  // Add more processing logic here
};

const startConsumer = async () => {
  try {
    await consumer.connect();
    console.log('Connected to Kafka broker');
    await consumer.subscribe({ topic: process.env.KAFKA_TOPIC || 'test-topic', fromBeginning: true });
    console.log('Subscribed to topic');

    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const msgValue = message.value.toString();
        console.log({ partition, offset: message.offset, value: msgValue });

        try {
          await processMessage(msgValue);
          // Acknowledge message processing if necessary
        } catch (error) {
          console.error('Error processing message:', error);
        }
      },
    });
  } catch (error) {
    console.error('Error in Kafka consumer:', error);
  }
};

const stopConsumer = async () => {
  try {
    await consumer.disconnect();
    console.log('Kafka consumer disconnected');
  } catch (error) {
    console.error('Error disconnecting Kafka consumer:', error);
  }
};

module.exports = { startConsumer, stopConsumer };

