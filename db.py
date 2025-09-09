import sqlite3
from sqlite3 import Error
import datetime

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
    # timestamp 必须为 UTC 格式字符串
    conn = create_connection(db_file)
    sql = ''' INSERT INTO ping_results(ip_address, response_time, timestamp)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (ip_address, response_time, timestamp))
    conn.commit()
    conn.close()
    return cur.lastrowid


def query_history(db_file, ip_list, period):
    if not isinstance(ip_list, list):
        ip_list = [ip_list]
    conn = create_connection(db_file)
    placeholders = ','.join(['?'] * len(ip_list))

    # 当前 UTC 时间
    now = datetime.datetime.utcnow()

    # 根据 period 算出起始时间
    if period == 'day':
        start_time = now - datetime.timedelta(days=1)
    elif period == 'week':
        start_time = now - datetime.timedelta(weeks=1)
    elif period == 'hour':
        start_time = now - datetime.timedelta(hours=1)
    else:
        conn.close()
        return []

    # 转换成字符串 (SQLite 常用格式: "YYYY-MM-DD HH:MM:SS")
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")

    sql = f'''
        SELECT * FROM ping_results
        WHERE ip_address IN ({placeholders})
          AND timestamp >= ?
        ORDER BY timestamp ASC
    '''
    cur = conn.cursor()
    cur.execute(sql, (*ip_list, start_time_str))
    result = cur.fetchall()
    conn.close()

    # 按 IP 分组返回
    grouped = {ip: [] for ip in ip_list}
    for row in result:
        ip = row[1]  # 假设 row[1] 是 ip_address
        if ip in grouped:
            grouped[ip].append(row)

    return grouped if len(ip_list) > 1 else grouped[ip_list[0]]