# Cory Learns Glue
A project used for me to learn how to use AWS Glue and other adventures in data analytics.

## Local ETL development

### Local environment setup
To perform local development, take the following steps to setup your environment:
1. You'll need python3 and Docker.
1. Go to the [etl](./etl) directory. All ETL source code lives here.
1. Setup a virtual environment: `python -m venv venv`.
1. Run `pip install -r requirements.txt`. This installs required dependencies.
1. Run `pip install -e .`. This ensures all modules in the ETL directory are available for tests, local runs, etc.
1. Run `./add-glue-modules.py`. This installs AWS Glue Python modules in your venv. It's annoying, but there isn't a pip-compatible way to install this that I know of.

### Run unit tests
To run unit tests, take these steps:
1. Ensure you've setup your environment using the [Local environment setup steps](#local-environment-setup).
1. Go to the [etl](./etl) directory.
1. Run `python -m pytest --ignore=integration-tests`. Notice that ignores integration-tests which require an actual Glue environment

## Run integration tests
To run integration tests, you'll need a Glue environment. You can use Docker to build that environment. Take the following steps to run all tests (unit and integration):
1. Go to the [etl](./etl) directory.
1. Ensure Docker is running on your machine.
1. Run `docker-compose -f integration-test.docker-compose.yml up --build`. This will launch a Glue environment and run all tests within that environment.
