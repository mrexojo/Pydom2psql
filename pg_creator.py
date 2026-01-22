import resources as rs
import sql
import logging

logger = logging.getLogger("Pydom2psql")

def db_creator(host, port, username, password, ndb, ntb, rows_input):
    """
    Creates multiple databases, tables, and populates them with random data.
    
    :param ndb: Number of databases to create
    :param ntb: Number of tables per database
    :param rows_input: Base number for rows (squared for total rows per table)
    """
    
    # Per README, rows are squared
    total_rows = rows_input * rows_input
    
    # Main loop for Databases
    for i in range(ndb):
        db_name = "itera_" + rs.rdm_string(4)
        
        # 1. Connect to default 'postgres' db to create new db
        conn_default = None
        try:
            conn_default = rs.pg_connect(host, port, username, password, "postgres")
            sql.create_database(conn_default, db_name)
        except Exception as e:
            logger.error(f"Skipping database setup due to creation error: {e}")
            continue
        finally:
            if conn_default:
                conn_default.close()
        
        # 2. Connect to the NEW database to create tables and data
        conn_new = None
        try:
            conn_new = rs.pg_connect(host, port, username, password, db_name)
            
            for j in range(ntb):
                tb_name = 'tb_' + rs.rdm_string(3)
                sql.create_table(conn_new, tb_name)
                
                # Insert Data
                logger.info(f"Generating {total_rows} rows for {db_name}.{tb_name}...")
                sql.insert_dummy_data(conn_new, tb_name, total_rows)
                
        except Exception as e:
             logger.error(f"Error processing database {db_name}: {e}")
        finally:
            if conn_new:
                conn_new.close()