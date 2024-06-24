const { Kafka } = require('kafkajs');

const kafka = new Kafka({
    clientId: 'backtest-producer',
    brokers: ['kafka:9092'], // Use the Docker service name 'kafka'
});

const producer = kafka.producer();

async function sendBacktestRequest(message) {
    await producer.connect();
    await producer.send({
        topic: 'backtest-requests',
        messages: [
            { value: JSON.stringify(message) }
        ]
    });
}

module.exports = sendBacktestRequest;
