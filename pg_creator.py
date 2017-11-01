#!/usr/bin/python
import psycopg2 as p
import logging
import resources as rs
import sql

log, xt_info = rs.it_logger()


# Iterative data creator - function
def db_creator(host, port, username, password, ndb, ntb, rpt):
    dbname = "postgres"
    conn = rs.pg_connect(host, port, username, password, dbname)
    cur = conn.cursor()
    conn.autocommit = True

    # Create DataBase
    print " Data creating..."
    for k in range(ndb):

        dbnam = "itera_" + rs.rdm_string(4)
        sql.mk_db(conn, cur, dbnam)
        cur.close()

        # Create Tables for new database
        for e in range(ntb):
            # connect to new dbnam "itera_"
            conn = rs.pg_connect(host, port, username, password, dbnam)
            cur = conn.cursor()
            tb_name = 'tb_' + rs.rdm_string(3)
            sql.mk_table(conn, cur, tb_name)

            # Insert Data for each table on new database
            for h in range(rpt):
                sql.insert_data(cur, tb_name, rpt)
                print "db: %s ->table: %s ->row: %d" % (dbnam, tb_name, h)

        cur.close()

    logging.info('Databases,Tables with data created', extra=xt_info)
