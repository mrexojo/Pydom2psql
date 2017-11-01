#!/usr/bin/python
import resources as rs
from psycopg2 import sql


# Delete quote on word - function
def no_q(wordq):
    word = wordq.replace('\'', '')
    return word


# Database Creator - function
def mk_db(conn, cur, dbname):
    dbnam = no_q(dbname)

    cur.execute("CREATE DATABASE %s ;" % dbnam)
    conn.commit()


# Table creator - function
def mk_table(conn, cur, tbname):
    tbnam = no_q(tbname)
    cols = "(col1 VARCHAR(12), col2 VARCHAR(12), col3 VARCHAR(12), col4 VARCHAR(12), col5 VARCHAR(12), col6 VARCHAR(12), col7 VARCHAR(12))"
    tbcreate = sql.SQL("CREATE TABLE {tb} {};").format(sql.Literal(no_q(cols)), tb=sql.Identifier(tbnam))

    # psycopg2 introduce quote on params. SQL needs no quote on "cols"
    clean_tbcreate = (no_q(tbcreate.as_string(conn)))
    # load table creation
    cur.execute(clean_tbcreate)


# Rows-Data creator - function
def insert_data(cur, tbnam, nrows):
    for h in range(nrows):

        p_list = list()
        for i in range(7):
            value = rs.rdm_string(12)
            p_list.insert(i, value)

        r_list = list()
        r_list.insert(h, p_list)

        s_list = ','.join(cur.mogrify('(%s,%s,%s,%s,%s,%s,%s);', x) for x in r_list)
        sql = """INSERT INTO {} (col1, col2, col3, col4, col5, col6, col7) VALUES """.format(tbnam)
        ins = sql + s_list

        cur.execute(ins)


# Databases count - function
def cl_db(cur, n):
    s_ndb = "SELECT datname FROM pg_database WHERE datname NOT IN ('template0','template1');"
    cur.execute(s_ndb)
    ndb = cur.rowcount
    l_db = cur.fetchall()
    if n > 0:
        return l_db
    else:
        return ndb


# Tables count - function
def cl_tb(cur, n):
    s_ntb = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
    cur.execute(s_ntb)
    ntb = cur.rowcount
    l_tb = cur.fetchall()
    if n > 0:
        return l_tb
    else:
        return ntb


# Total & Average rows - function
def total_rws(cur, host, port, username, password):

    # Iterate rows by db list
    total_rwdbs = 0
    dblist = cl_db(cur, 1)

    for z in range(cl_db(cur, 0)):

        namdb = (dblist[z])
        nmdb = ''.join(map(str, namdb))
        print "----------"
        print "Database: " + str(nmdb)
        cur.close()
        # Connect to db
        conn = rs.pg_connect(host, port, username, password, nmdb)
        cur = conn.cursor()

        total_rwdb = 0
        total_tb = cl_tb(cur, 0)
        tblist = cl_tb(cur, 1)

        # Iterate total rows per table
        for f in range(total_tb):
            tb = ''.join(map(str, tblist[f]))
            rws_table = "SELECT reltuples::bigint AS rws FROM pg_class WHERE oid = '%s'::regclass;" % tb
            cur.execute(rws_table)
            trw = cur.fetchone()
            # String to integer cleaner
            ctrw = ''.join(map(str, trw))
            st2int = int(ctrw)
            # Sum rows each table
            total_rwdb += st2int

        # Sum & average rows per db
        print "Total rows: " + str(total_rwdb)
        print "Total tables: " + str(total_tb)
        if total_tb > 0:
            avarows = total_rwdb / total_tb
            print "Average rows: " + str(avarows)
        else:
            print "N/A"

        # Sum total rows of all dbs
        total_rwdbs += total_rwdb
    print "------------------------------"
    print "Total rows PostgreSQL server: " + str(total_rwdbs)
