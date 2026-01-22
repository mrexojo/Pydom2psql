import argparse
import getpass
import sys
import os
import resources as rs
import sql
from psycopg2 import sql as psql

logger = rs.setup_logger()

def get_db_stats(host, port, user, password, db_name):
    """Connects to a specific DB and counts tables and total rows."""
    conn = None
    try:
        conn = rs.pg_connect(host, port, user, password, db_name)
        
        # Get all tables in public schema
        query_tables = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        tables = []
        with conn.cursor() as cur:
            cur.execute(query_tables)
            tables = [row[0] for row in cur.fetchall()]
            
        total_rows = 0
        table_count = len(tables)
        
        for tb in tables:
            rows = sql.count_rows(conn, tb)
            total_rows += rows
            # logger.info(f"  - Database {db_name} | Table {tb}: {rows} rows")
            
        return table_count, total_rows

    except Exception as e:
        logger.error(f"Failed to check database {db_name}: {e}")
        return 0, 0
    finally:
        if conn:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description="Check statistics of generated PostgreSQL databases.")
    
    parser.add_argument("--ip", help="PostgreSQL Host IP", default=os.getenv("PG_HOST", "localhost"))
    parser.add_argument("--port", help="PostgreSQL Port", type=int, default=int(os.getenv("PG_PORT", 5432)))
    parser.add_argument("--user", help="PostgreSQL User", default=os.getenv("PG_USER", "postgres"))
    parser.add_argument("--password", help="PostgreSQL Password", default=os.getenv("PG_PASSWORD", None))
    parser.add_argument("--pattern", help="Database name pattern to search", default="itera_%")

    args = parser.parse_args()

    password = args.password
    if not password:
        try:
            password = getpass.getpass(f"Password for {args.user}: ")
        except (EOFError, KeyboardInterrupt):
            sys.exit(1)

    # 1. Connect to postgres to list databases
    try:
        conn = rs.pg_connect(args.ip, args.port, args.user, password, "postgres")
        
        # Find databases matching pattern
        pattern_query = "SELECT datname FROM pg_database WHERE datname LIKE %s"
        target_dbs = []
        with conn.cursor() as cur:
            cur.execute(pattern_query, (args.pattern,))
            target_dbs = [row[0] for row in cur.fetchall()]
        
        conn.close()
        
        logger.info(f"Found {len(target_dbs)} databases matching '{args.pattern}'")
        
        grand_total_rows = 0
        grand_total_tables = 0
        
        for db in target_dbs:
            t_count, r_count = get_db_stats(args.ip, args.port, args.user, password, db)
            grand_total_tables += t_count
            grand_total_rows += r_count
            logger.info(f"Database: {db} | Tables: {t_count} | Total Rows: {r_count}")

        logger.info("="*40)
        logger.info(f"SUMMARY")
        logger.info(f"Total Databases: {len(target_dbs)}")
        logger.info(f"Total Tables:    {grand_total_tables}")
        logger.info(f"Total Rows:      {grand_total_rows}")
        logger.info("="*40)

    except Exception as e:
        logger.error(f"Error during check: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()