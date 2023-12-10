import argparse
import socket
import sys
import getpass
import logging as log

# Argument parser
psr = argparse.ArgumentParser(description="This script connects to a PostgreSQL database.")
psr.add_argument("--ip", help="IP address of the database", required=True)
psr.add_argument("--user", help="Username for the database", required=True)
psr.add_argument("--count", help="Count of databases", type=int, default=1)
psr.add_argument("--tables", help="Total tables per db", type=int, default=1)
psr.add_argument("--rows", help="Rows Squared per table", type=int, default=10)
psr.add_argument("--port", help="Port db", type=int, default=5432)
psr.add_argument("--db", help="Database name", required=True)

dat = psr.parse_args()

# Socket creation
s = socket.socket()
s.settimeout(3)

try:
    s.connect((dat.ip, dat.port))
except socket.error as exc:
    log.error(f"Connection Error: {exc}")
    sys.exit(1)

# User Password
print(f"{dat.user} user")
pwd = getpass.getpass()

# Database connection
try:
    conn = rs.pg_connect(dat.ip, dat.port, dat.user, pwd, dat.db)
    cur = conn.cursor()
    log.info("Connected to Postgresql!", extra=xt_info)
    sql.total_rws(cur, dat.ip, dat.port, dat.user, pwd)
except Exception as e:
    log.error(f"Database connection error: {e}")
    sys.exit(1)

# Remember to close connections when done
finally:
    s.close()
    if conn:
        conn.close()


if __name__ == "__main__":
    check()