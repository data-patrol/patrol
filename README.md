# patrol

Hello and welcome!

We are a small team of data enthusiasts building a lightweight data quality tool. The general idea is that it will help to execute data quality checks across multiple data sources and help to monitor and manage data quality. With the right use, we think it can bring data quality to the next level!

The tool will come with a simple web UI and will initially support the following data sources:

- Redshift
- Snowflake
- SQL Server
- Oracle 
- MySQL / MariaDB
- PostgreSQL
- Databricks
- Presto/Trino

The tool will be available in form of a Docker image, so it can easily run in any cloud and on-prem.

The first release (rc1) is expected some time between June and November 2023. Stay tuned!

You can reach out to us if you are interested in contribution to the project - smirnov860860@gmail.com.

## Run locally

### Prepare
1. checkout git repo `https://github.com/data-patrol/patrol`, all subsequent commands assume you're in repo root
2. install Python 3.9+ `python3 --version`
3. install Python libraries `pip3 install -r requirements.txt`

### Configure
1. Create a home directory for patrol project, like `mkdir ~/patrol`. This directory will be used as:
   1. Home directory for SQLite DB (file `patrol.db`)
   2. Home directory for project configuration 
2. Set env variable `PATROL_HOME` if differ from default `~/patrol`
3. Create configuration or copy test one `cp -r test_data/checks $PATROL_HOME`
4. Initialize DB `patrol/bin> python3 patrol initdb`

### Test
PATROL_HOME/patrol.cfg - where to find checks
`patrol/bin> python3 patrol test`

### Usage
Run check by id `patrol/bin> python3 patrol run {check_id}`
will search checks according to patrol.cfg
