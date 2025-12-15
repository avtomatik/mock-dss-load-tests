# Digital Signature Service Locust Tests

This project contains **Locust** load tests for the **Digital Signature Service** project. It is designed to evaluate the performance and scalability of the digital signature service under various conditions, simulating real-world traffic.

## Prerequisites

* Docker
* Docker Compose
* Access to the **mock-dss** repository

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

Ensure you have both the `mock-dss` and `mock-dss-load-tests` repositories.

```bash
git clone <mock-dss-repository-url>
git clone <mock-dss-load-tests-repository-url>
```

### Build and Run Docker Containers Locally

Make sure you have Docker and Docker Compose installed. To run the tests locally, follow these steps:

1. From the **`mock-dss`** repository, run the following command:

```bash
sudo docker-compose up --build
```

This will:

1. Build the Docker images.
2. Set up the required services (e.g., Backend, PostgreSQL, RabbitMQ).

### Configuration

Before running the tests, you need to configure your local environment:

1. Copy the example environment file to `.env.local`:

```bash
cp .env.local.example .env.local
```

2. Open `.env.local` and update the following configurations:

   * Set the `default_pass` to the required password.
   * Ensure the service names are updated to use `localhost` instead of other hostnames.

Test configurations such as the number of users, spawn rate, and test duration can be modified in the `pyproject.toml` file, under the `[tool.locust]` section.

### Setting Up the Virtual Environment

After configuring your environment, you can set up the virtual environment and sync the dependencies:

```bash
# Create and activate a virtual environment
uv venv
source .venv/bin/activate

# Sync dependencies
uv sync
```

### Running Locust

Once your environment is set up and dependencies are synced, you can start the Locust load tests by running:

```bash
uv run locust
```

This will start the Locust service, and you’ll be able to access the web interface.

## Running the Tests

Once the Docker containers are up and Locust is running, you can access the Locust web interface at `http://localhost:8089` to configure and start the load tests.

1. Specify the number of virtual users (clients), spawn rate, and target endpoints.
2. Click **Start swarming** to begin the load test.

Locust will simulate traffic on your **Digital Signature Service** and provide real-time results.

## Results

Locust provides a dashboard with key metrics such as:

* Request/response latency (min, avg, max)
* Requests per second
* Failure rate
* Response times for different HTTP methods and endpoints

These metrics will help you assess the performance of the system under load.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---
