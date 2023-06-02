# patrol

Hello and welcome!

We are a small team of data enthusiasts building a lightweight data quality tool. The idea is that it will help to execute data quality checks across multiple data sources and help to proactively monitor and manage data quality. 

The tool will come with a simple web UI and will eventually support the following data sources:

- PostgreSQL
- SQL Server
- Oracle 
- MySQL / MariaDB
- Redshift
- Snowflake
- Databricks
- Presto/Trino

The tool will be available in form of a Docker image, so it can easily run in any cloud and on-prem.
You can reach out to us if you are interested in contribution to the project - smirnov860860@gmail.com.

## Run using Docker

### Prepare
1. Install Docker
2. Checkout git repo `https://github.com/data-patrol/patrol`, all subsequent commands assume you're in repo root

### Run
Run the following command from the repo root directory "docker-compose up -d"

### Test
Using Docker CLI (or Docker Desktop) connect to pt_ptapp_1 container and run the following commands:
cd /app/patrol/bin
python test test

### Usage
Run check by id `patrol/bin> python3 patrol run {check_id}`
will search checks according to patrol.cfg
