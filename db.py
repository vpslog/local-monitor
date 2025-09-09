import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(db_file):
    conn = create_connection(db_file)
    try:
        sql_create_ping_results_table = """ CREATE TABLE IF NOT EXISTS ping_results (
                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                ip_address TEXT NOT NULL,
                                                response_time REAL,
                                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                                            ); """
        cursor = conn.cursor()
        cursor.execute(sql_create_ping_results_table)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            
def insert_ping_result(db_file, ip_address, response_time, timestamp):
    conn = create_connection(db_file)
    sql = ''' INSERT INTO ping_results(ip_address, response_time, timestamp)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (ip_address, response_time, timestamp))
    conn.commit()
    conn.close()
    return cur.lastrowid

def query_history(db_file, ip_address, period):
    conn = create_connection(db_file)
    sql = ''' SELECT * FROM ping_results WHERE ip_address = ? AND timestamp >= datetime('now', ?) '''
    cur = conn.cursor()
    if period == 'day':
        cur.execute(sql, (ip_address, '-1 day'))
    elif period == 'week':
        cur.execute(sql, (ip_address, '-7 days'))
    elif period == 'month':
        cur.execute(sql, (ip_address, '-30 days'))
    else:
        conn.close()
        return []
    result = cur.fetchall()
    conn.close()
    return result
