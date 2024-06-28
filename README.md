# Project README

## Project Overview

This project aims to build a scalable and reliable cryptocurrency trading data pipeline using Kafka for real-time data streaming and backtesting. The system will integrate various backend components to handle data ingestion, processing, and analysis, supporting Mela's objective of providing a user-friendly platform for cryptocurrency investors.

## Task Description

### Task 3: Backend Development for Kafka Integration

In this task, our goal is to develop backend components in Python that integrate with Kafka to manage backtest parameters and results efficiently. We will implement Kafka consumers and producers, business logic services, and data models to support the trading data pipeline.

### Responsibilities

- Implement Kafka consumers (`backtest_consumer.py`) to handle incoming backtest parameters (`backtest_parameters`).
- Develop Kafka producers (`backtest_producer.py`) to publish messages with backtest results (`backtest_results`).
- Design and implement backend services (`backtest_service.py`) to execute backtests based on received parameters and store results.
- Configure Kafka settings (`kafka_config.py`) and utilities (`kafka_utils.py`) for seamless integration.
- Ensure modular design and clear documentation to facilitate integration with frontend and database components.


### Installation and Setup

#### Prerequisites

- Python 3.x installed on your system.
- Kafka broker URL and configuration details.

#### Installation Steps

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd backend
    ```
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Configure Kafka settings in config/kafka_config.py.

4. Run the backend application:
    
    ```bash
    python src/main.py
    ```

## Testing
To ensure the functionality and reliability of backend components, automated tests (test/test_files.py) have been implemented to validate Kafka integration, data processing logic, and system performance.

## Integration Phase
After completing backend development tasks, integrate with frontend components and databases developed by other team members:

Update README and documentation to reflect integrated components.
Conduct integration testing to verify communication between frontend, backend, and data sources.

## Best Practices
Maintain modular design and clear naming conventions for files and directories.
Use version control (Git) for collaboration and code management.
Document extensively to facilitate understanding and future maintenance.

## Resources
Python Kafka Documentation
Apache Kafka Documentation

## License
Specify the project's license (if applicable) and any terms of use or redistribution.

## Contact

export FLASK_APP=app
export FLASK_ENV=development
flask run