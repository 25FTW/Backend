import sqlite3
from sqlite3 import Error


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


database = "cashflowManagement.db"
conn = create_connection(database)

registerTable = """CREATE TABLE IF NOT EXISTS register (
username text PRIMARY KEY NOT NULL,pswd text);"""

datatable = """CREATE TABLE IF NOT EXISTS data (
username text NOT NULL ,category text, actual_item text, cost text, date text,
FOREIGN KEY (username) REFERENCES registerTable (username));
"""

budgetTable = """CREATE TABLE IF NOT EXISTS budgetTable (
username text NOT NULL PRIMARY KEY,budget text,
FOREIGN KEY (username) REFERENCES registerTable (username));
"""

logs = """CREATE TABLE IF NOT EXISTS logs (
username text NOT NULL ,log text,
FOREIGN KEY (username) REFERENCES registerTable (username));
"""

if conn:
    create_table(conn, registerTable)
    create_table(conn, datatable)
    create_table(conn, budgetTable)
    create_table(conn, logs)
else:
    print("cannot create tables.")
