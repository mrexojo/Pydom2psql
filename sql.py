#!/usr/bin/python
import resources as rs
from psycopg2 import sql

# Remove quotes from a string - function
def no_q(wordq):
    return wordq.replace('\'', '')

# Database Creator - function
def mk_db(conn, cur, dbname):
    dbnam = no_q(dbname)
    try:
        cur.execute("CREATE DATABASE %s ;" % dbnam)
        conn.commit()
    except Exception as e:
        logging.error(f"Database creation error: {e}")

# Table creator - function
def mk_table(conn, cur, tbname):
    tbnam = no_q(tbname)
    cols = "(col1 VARCHAR(12), col2 VARCHAR(12), col3 VARCHAR(12), col4 VARCHAR(12), col5 VARCHAR(12), col6 VARCHAR(12), col7 VARCHAR(12))"
    tbcreate = sql.SQL("CREATE TABLE {tb} {};").format(sql.Literal(no_q(cols)), tb=sql.Identifier(tbnam))

    # psycopg2 introduce quote on params. SQL needs no quote on "cols"
    clean_tbcreate = (no_q(tbcreate.as_string(conn)))
    # load table creation
    try:
        cur.execute(clean_tbcreate)
    except Exception as e:
        logging.error(f"Table creation error: {e}")