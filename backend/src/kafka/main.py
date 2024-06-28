from utils.kafka_utils import create_kafka_topics

def main():
    # Create Kafka topics if they do not exist
    create_kafka_topics()

    # Add your main application logic here

if __name__ == "__main__":
    main()
