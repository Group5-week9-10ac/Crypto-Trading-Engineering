const { Kafka } = require('kafkajs');

const kafka = new Kafka({
    clientId: 'my-app',
    brokers: ['kafka:9092'], // Use the Docker service name 'kafka'
});

const consumer = kafka.consumer({ groupId: 'test-group' });

const startConsumer = async () => {
  try {
    await consumer.connect();
    console.log('Connected to Kafka broker');
    await consumer.subscribe({ topic: 'test-topic', fromBeginning: true });
    console.log('Subscribed to topic');

    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        console.log({
          partition,
          offset: message.offset,
          value: message.value.toString(),
        });
      },
    });
  } catch (error) {
    console.error('Error in Kafka consumer:', error);
  }
};

module.exports = startConsumer;
