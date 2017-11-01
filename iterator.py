#!/usr/bin/python
import sys
import socket
import argparse
import getpass
import pg_creator
import resources as rs

log, xt_info = rs.it_logger()


def main():
    psr = argparse.ArgumentParser()
    # Required arguments
    req = psr.add_argument_group('Use Required')
    req.add_argument("--ip", help="IP address Postgresql server ", required=True)
    req.add_argument("--user", help="Username", required=True)

    # Optional arguments
    psr.add_argument("--count", help="Total dbs to create", type=int, default=1)
    psr.add_argument("--tables", help="Total tables per db", type=int, default=1)
    psr.add_argument("--rows", help="Rows Squared per table", type=int, default=10)
    psr.add_argument("--port", help="Port db", type=int, default=5432)

    dat = psr.parse_args()
    ip = dat.ip
    user = dat.user
    count = dat.count
    tables = dat.tables
    rows = dat.rows
    port = dat.port

    if not dat.ip or not dat.user:
        log.error('Please, for help use with -h or --help argument', extra=xt_info)
        sys.exit(1)

    else:
        s = socket.socket()
        s.settimeout(3)

        try:
            s.connect((dat.ip, dat.port))
        except socket.error, exc:
            print "Connection Error: " % exc
            sys.exit(1)

    # User Password
    print dat.user + " user"
    pwd = getpass.getpass()

    try:
        # Data Creator
        pg_creator.db_creator(ip, port, user, pwd, count, tables, rows)
        log.info("Finished data creation", extra=xt_info)
    except:
        print
        log.exception("Fail data creation", extra=xt_info)


if __name__ == "__main__":
    main()
