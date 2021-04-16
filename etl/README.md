# Cory Learns Glue - ETL
This folder contains all source code and corresponding tests for the Glue ETLs.

## Local ETL development
This section outlines instructions for machine setup for local development and automated testing of the ETL source code.

### Local environment setup
To perform local development, take the following steps to setup your environment:
1. You'll need [python](https://www.python.org/downloads/) and [Docker Compose](https://docs.docker.com/compose/install/).
1. Setup a virtual environment: `python -m venv venv`.
1. Run `pip install -r requirements.txt`. This installs required dependencies.
1. Run `pip install -e .`. This ensures all modules in the ETL directory are available for tests, local runs, etc.
1. Run `./add_glue_modules.py`. This installs AWS Glue Python modules in your venv. It's annoying, but there isn't a pip-compatible way to install this that I know of.

### Run unit tests
To run unit tests, take these steps:
1. Ensure you've setup your environment using the [Local environment setup steps](#local-environment-setup).
1. Run `python -m pytest --ignore=integration_tests`. Notice that ignores integration-tests which require an actual Glue environment

## Run integration tests
Integration tests depend on Spark and a Glue environment. You can use Docker to build that environment
and then run all integration tests within the Docker environment. Take the following steps to run all tests
(unit and integration):
1. Ensure Docker is running on your machine.
1. Run `docker-compose -f integration-tests.docker-compose.yml up --build`. This will launch a Glue environment
git and run all tests within that environment.
