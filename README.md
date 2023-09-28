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

### mypy static type enforcement
- Check: `mypy --namespace-packages --install-types .`
- Fix problems by fixing inconsistent typing

### Flake8 Styleguide Enforcement
- Check: `flake8 .`
- Fix the displayed problems manually in the files

### Black Styleguide Enforcement
- Check: `black --line-length 120 --check .`
- Fix problems using the black auto formatter:
  - Installation: File -> Settings -> Tools -> External Tools -> "+" -> add "Black"
    - Program: `~/.local/share/virtualenvs/fairq-data-dwd-xxxx/bin/black` (adjust for your VE path)
    - Arguments: `$FilePath$ --line-length 120`
    - Working directory: `$ProjectFileDir$`
  - Add a shortkey to run the auto formatter, e.g., CTRL+SHIFT+A

### isort: order of import statements
- Fix problems via `isort .`

### Example workflow:
1. Always use Black CTRL+SHIFT+A to fix formatting errors
2. use `isort .` to fix import errors
3. use `flake8 .` and fix missing docstrings, trailing commas and other small things
4. use `flake8 .` and fix remaining complexity errors.
5. In case flake 8 is really wrong (mostly it is not) you can whitelist an error by adding `# noqa: WPS123` to the line
