import argparse
import getpass
import sys
import os
import pg_creator
import resources as rs

logger = rs.setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Generate random data in PostgreSQL.")
    
    # Connection args
    parser.add_argument("--ip", help="PostgreSQL Host IP", default=os.getenv("PG_HOST", "localhost"))
    parser.add_argument("--port", help="PostgreSQL Port", type=int, default=int(os.getenv("PG_PORT", 5432)))
    parser.add_argument("--user", help="PostgreSQL User", default=os.getenv("PG_USER", "postgres"))
    parser.add_argument("--password", help="PostgreSQL Password", default=os.getenv("PG_PASSWORD", None))
    
    # Workload args
    parser.add_argument("--count", help="Total databases to create", type=int, default=1)
    parser.add_argument("--tables", help="Total tables per database", type=int, default=1)
    parser.add_argument("--rows", help="Base number for rows (will be squared)", type=int, default=10)

    args = parser.parse_args()

    # Password handling: CLI arg > Env Var > Interactive Prompt
    password = args.password
    if not password:
        try:
            password = getpass.getpass(f"Password for {args.user}: ")
        except (EOFError, KeyboardInterrupt):
            logger.error("Operation cancelled.")
            sys.exit(1)

    logger.info(f"Starting generation: {args.count} DBs, {args.tables} tables/db, {args.rows}^2 rows/table")

    try:
        pg_creator.db_creator(
            host=args.ip,
            port=args.port,
            username=args.user,
            password=password,
            ndb=args.count,
            ntb=args.tables,
            rows_input=args.rows
        )
        logger.info("Data generation completed successfully.")
    except Exception as e:
        logger.error(f"Critical error during generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()