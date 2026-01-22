import os
import logging
import psycopg2
import random
import string
from typing import Optional

# Configuration for logging
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger("Pydom2psql")

logger = setup_logger()

def get_env_variable(name: str, default: Optional[str] = None) -> str:
    val = os.getenv(name, default)
    if val is None:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return val

def pg_connect(host, port, user, password, dbname, autocommit=True):
    """
    Establish a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        conn.autocommit = autocommit
        return conn
    except psycopg2.Error as e:
        logger.error(f"Connection failed: {e}")
        raise

def rdm_string(length: int = 8) -> str:
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))