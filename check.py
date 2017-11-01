#!/usr/bin/python
import sys
import socket
import argparse
import getpass
import logging
import resources as rs
import sql

log, xt_info = rs.it_logger()


def check():
    psr = argparse.ArgumentParser()
    # Required arguments
    req = psr.add_argument_group('Use Required')
    req.add_argument("--ip", help="IP address Postgresql server ", required=True)
    req.add_argument("--user", help="Username", required=True)

    # Optional arguments
    psr.add_argument("--port", help="Port db", type=int, default=5432)
    psr.add_argument("--db", help="Dbname", default="postgres")
    psr.add_argument("--")
    chk = psr.parse_args()
    ip = chk.ip
    user = chk.user
    port = chk.port
    dbname = chk.db

    if not chk.ip or not chk.user:
        logging.error('Please, for help use with -h or --help argument', extra=xt_info)
        sys.exit(1)

    else:
        s = socket.socket()
        s.settimeout(3)

        try:
            s.connect((chk.ip, chk.port))
        except socket.error, exc:
            print "Connection Error: " % exc
            sys.exit(1)

    # User Password
    print chk.user + " user"
    pwd = getpass.getpass()

    if pwd:
        conn = rs.pg_connect(ip, port, user, pwd, dbname)
        cur = conn.cursor()
        log.info("Connected to Postgresql!", extra=xt_info)
        sql.total_rws(cur, ip, port, user, pwd)


if __name__ == "__main__":
    check()
