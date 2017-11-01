# Pyrandom2postgre
------------
PyRandom to Postgresql
------------

Concept test is generate random data on PostgreSQL server and check some parameters of server.
You can check number tables, rows and average rows per database, calculating the total rows of Postgresql server at the end of output.

Verions of tools used:

SO: Centos 7.3
PostgreSQL 9.2.18
Python 2.7
psycopg2: 2.7.3.1


Content:

    - iterator.py
    - check.py
    - pg_creator.py
    - sql.py
    - resources.py


iterator.py
---------

Python script for generate random data from server or client with tools.
The arguments required are --ip for ip address (or localhost from server), and --user for username of PostgreSQL for connect.
Password always is a interactive input. If not use optional arguments, itera.py generates random data on the next distribution:

    1 database
    1 table
    100 rows

(1 row = 8 columns of 12 random characters for each.)

This program use pg_creator.py for an iterate creation of data, and this use sql.py for sql sentences. Both are using resources.py for connection, random name of databases or tables.

For more speed, the number of rows per table are squared, therefore the next command :

    iterator.py --ip 192.168.49.78 --user postgres --rows 50

You'll generate:

    1 database
    1 table
    2500 rows

DATA GENERATION USE
-------
usage: iterator.py [-h] --ip IP --user USER [--count COUNT] [--tables TABLES]
                 [--rows ROWS] [--port PORT]

optional arguments:
  -h, --help       show this help message and exit
  --count COUNT    Total dbs to create
  --tables TABLES  Total tables per db
  --rows ROWS      Rows Squared per table
  --port PORT      Port db

Use Required:
  --ip IP          IP address Postgresql server
  --user USER      Username

example:

    python iterator.py --ip 192.168.49.78 --user postgres

output:
    postgres user
    Password:
     Data creating...
    db: itera_llmn ->table: tb_lxy ->row: 0
    db: itera_llmn ->table: tb_lxy ->row: 1
    db: itera_llmn ->table: tb_lxy ->row: 2
    db: itera_llmn ->table: tb_lxy ->row: 3
    ....
    ...
    .

CHECK
-----

Check.py is a python script which show number tables, rows and average rows per database,
calculating the total rows of Postgresql server at the end of output.
Execution of this script it's similar to itera.py

example:

    python check.py --ip 192.168.49.78 --user postgres

output:
    postgres user
    Password:

    ----------
    Database: itera_lhpg
    Total rows: 23328
    Total tables: 8
    Average rows: 2916
    ----------
    ....
    ...
    ..
    .
    Database: itera_jdum
    Total rows: 7200
    Total tables: 2
    Average rows: 3600
    ----------
    Database: itera_frps
    Total rows: 45916
    Total tables: 1
    Average rows: 45916
    ----------
    Database: itera_thod
    Total rows: 112906
    Total tables: 12
    Average rows: 9408
    ------------------------------
    Total rows PostgreSQL server: 1208455


Clear
------
For clean databases created by iterator.py, at the moment execute from bash shell Postgresql server (as postgres user or allowed user):

    for i in `psql -l | awk {'print $1'} | grep itera_`; do dropdb $i; done

