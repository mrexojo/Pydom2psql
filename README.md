# Pydom2psql - Dockerized

Python scripts to generate random PostgreSQL databases, tables, and data for performance testing or verification.

## Features

- **Safe & Secure**: Uses parameterized queries and environment variables for credentials.
- **Dockerized**: specific `Dockerfile` and `docker-compose` setup for instant usage.
- **Automated**: Generates multiple DBs and tables with a squared number of rows pattern.
- **Verification**: `check.py` scans the server to report total stats for generated data.

## Project Structure

- `iterator.py`: Main entry point for generating data.
- `check.py`: Tool to verify and count generated data.
- `pg_creator.py` & `sql.py`: Core logic for DB operations.
- `resources.py`: Shared utilities (logging, connection).

## Getting Started (Docker)

1. **Start the Environment**
   ```bash
   docker compose up -d
   ```
   This starts a PostgreSQL 15 container and an app container.

2. **Generate Data**
   Run the generator inside the app container:
   ```bash
   # Generate 2 Databases, 2 Tables each, 10^2=100 rows per table
   docker compose exec app python iterator.py --count 2 --tables 2 --rows 10
   ```
   *Note: Authentication is handled automatically via environment variables defined in `docker-compose.yml`.*

3. **Check Statistics**
   Run the checker to see what was created:
   ```bash
   docker compose exec app python check.py
   ```

4. **Cleanup**
   To stop and remove containers (and data volume):
   ```bash
   docker compose down -v
   ```

## Local Usage

If you prefer running locally (requires Python 3.9+ and PostgreSQL running):

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run scripts:
   ```bash
   # Set env vars or pass args
   export PG_PASSWORD=mysecretpassword
   python iterator.py --ip localhost --user postgres --count 1
   ```
