#!/usr/bin/python
import psycopg2 as p
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import getpass
import logging
import random
import string


# Connector Postgres server - function
def pg_connect(host, port, username, password, dbname):
    xt_info = it_logger()
    try:

        conn = p.connect(user=username, password=password, host=host, port=port, database=dbname)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    except Exception as err:
        logging.error(err, extra=xt_info)
        raise

    return conn


def rdm_string(x):
    # generates x ramdom chars
    return ''.join(random.choice(string.ascii_lowercase) for i in range(x))


def it_logger():
    # Logging Info
    username = getpass.getuser()
    fmat = '%(asctime)-15s %(user)-8s %(message)s'
    logging.basicConfig(format=fmat)
    xt_info = {'user': username}
    logger = logging.getLogger('itera_logger')

    return logger, xt_info
