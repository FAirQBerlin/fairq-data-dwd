# FAirQ Data DWD (Deutscher Wetterdienst)

Code to extract weather data from https://brightsky.dev/ and write it to a Clickhouse database.


## How to get started
- Create an .env file in the project folder, see `env_template` for the structure
- Create database as described in https://github.com/fairqBerlin/fairq-data/tree/main/inst/db (schema fairq_raw)

## Most important files
- `get_dwd_observations.py`: This script queries the historic dwd data since a given date until today and writes it to
the clickhouse db. Default is the last 2 days to make sure that we don't have any gaps if the process does not run for a day.
- `historize_forecasts.py`: This script queries dwd forecasts for the next 5 days and historizes them in the clickhouse db.


## Input and output

### Input

- API https://brightsky.dev/

### Output

- Database, schema `fairq_raw`

## Style checking

The Jenkins file of this repo contains rigorous style checking. You can run those checks
in the console as well. This sections lists the checks and tells how to fix problems.

### Mypy Static Type Enforcement
- Check: `mypy --namespace-packages --install-types .`
- Fix problems by fixing inconsistent typing

### Ruff Styleguide Enforcement
- Formatting: `ruff format .`
- Check: `ruff check .`
- Fix the displayed problems manually in the files
