# Digital Signature Service Locust Tests

This project contains **Locust** load tests for the **Digital Signature Service** project. It is designed to evaluate the performance and scalability of the digital signature service under various conditions, simulating real-world traffic.

## Prerequisites

* Docker
* Docker Compose
* Access to the **digital-signature-service** repository

## Project Structure

```
.
├── clients
│   ├── postgresql.py  # PostgreSQL client for load testing
│   ├── rabbitmq.py    # RabbitMQ client for load testing
│   └── redis.py       # Redis client for load testing
├── core
│   ├── config.py      # Configuration settings for the tests
│   ├── constants.py   # Constants used in the tests
│   ├── helpers.py     # Helper functions
│   └── users.py       # User logic for Locust tests
├── docker-compose.override.yml  # Locust service config for Docker Compose
├── Dockerfile         # Docker image build file
├── LICENSE.md         # License for the project
├── locustfile.py      # Main Locust load testing script
├── pyproject.toml     # Python project metadata and dependencies
└── README.md          # This file
```

## Setup

### Clone the Repositories

Ensure you have both the `digital-signature-service` and `digital-signature-service-locust-tests` repositories.

```bash
git clone <digital-signature-service-repository-url>
git clone <digital-signature-service-locust-tests-repository-url>
```

### Build and Run Docker Containers

Make sure you have Docker and Docker Compose installed. To run the tests, use the `docker-compose.override.yml` file from this repository in conjunction with the main `docker-compose.yml` file from the sibling `digital-signature-service` repository.

From the **`digital-signature-service`** repository, run the following command:

```bash
sudo docker-compose -f docker-compose.yml -f ../digital-signature-service-locust-tests/docker-compose.override.yml up --build
```

This command will:

1. Build the Docker images.
2. Set up the required services (e.g., Locust, PostgreSQL, RabbitMQ).
3. Start running the Locust load tests.

### Configuration

The configuration of the tests can be adjusted in the `core/config.py` file. You can modify parameters such as the number of users, spawn rate, and test duration to suit your needs.

## Running the Tests

Once the Docker containers are up, you can access the Locust web interface at `http://localhost:8089` to configure and start the load tests.

* Specify the number of virtual users (clients), spawn rate, and target endpoints.
* Click **Start swarming** to begin the load test.

Locust will then simulate traffic on your **Digital Signature Service** and provide real-time results.

## Results

Locust provides a dashboard with key metrics such as:

* Request/response latency (min, avg, max)
* Requests per second
* Failure rate
* Response times for different HTTP methods and endpoints

These metrics will help you assess the performance of the system under load.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
