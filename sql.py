from psycopg2 import sql, extras
import random
import logging
import resources as rs

logger = logging.getLogger("Pydom2psql")

def create_database(conn, db_name):
    """Creates a new database safely using sql identifiers."""
    try:
        with conn.cursor() as cur:
            # FORCE_FIRST: cannot run CREATE DATABASE inside a transaction block if not autocommit
            # conn.autocommit should be True from resources.pg_connect
            query = sql.SQL("CREATE DATABASE {};").format(sql.Identifier(db_name))
            cur.execute(query)
            logger.info(f"Database created: {db_name}")
    except Exception as e:
        logger.error(f"Error creating database {db_name}: {e}")
        # We might continue if it already exists, or raise
        pass

def create_table(conn, table_name):
    """Creates a table with 8 varchar columns."""
    columns = [f"col{i}" for i in range(1, 9)]
    
    # Construct column definitions: col1 VARCHAR(12), col2 VARCHAR(12)...
    col_defs = sql.SQL(", ").join(
        [sql.SQL("{} VARCHAR(12)").format(sql.Identifier(c)) for c in columns]
    )

    query = sql.SQL("CREATE TABLE {} ({});").format(
        sql.Identifier(table_name),
        col_defs
    )

    try:
        with conn.cursor() as cur:
            cur.execute(query)
            logger.info(f"Table created: {table_name}")
    except Exception as e:
        logger.error(f"Error creating table {table_name}: {e}")
        raise

def insert_dummy_data(conn, table_name, num_rows):
    """Inserts dummy data into the table."""
    # Generate data: List of tuples
    # each tuple has 8 random strings
    data = []
    
    # Generate data in memory (watch out for huge num_rows, but usually it is small-ish for this tool)
    # The READMe mentions 'Rows Squared' so if input is 50, rows=2500 per table.
    
    for _ in range(num_rows):
        row = tuple(rs.rdm_string(12) for _ in range(8))
        data.append(row)

    columns = [f"col{i}" for i in range(1, 9)]
    
    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(map(sql.Identifier, columns))
    )

    try:
        with conn.cursor() as cur:
            extras.execute_values(cur, insert_query, data)
            logger.info(f"Inserted {num_rows} rows into {table_name}")
    except Exception as e:
        logger.error(f"Error inserting data into {table_name}: {e}")
        raise

def count_rows(conn, table_name):
    query = sql.SQL("SELECT count(*) FROM {}").format(sql.Identifier(table_name))
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchone()[0]
    except Exception as e:
        logger.error(f"Error counting rows in {table_name}: {e}")
        return 0