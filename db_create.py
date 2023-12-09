import sqlite3

from config import db

sql_create_groups_table = \
    """
    CREATE TABLE IF NOT EXISTS Groups (
        id bigint PRIMARY KEY,
        gr integer,
        thread_stats integer,
        thread_mathhedgehog integer,
        thread_profkomvmk integer
    );
    """
sql_create_students_table = \
    """
    CREATE TABLE IF NOT EXISTS Students (
        id integer PRIMARY KEY,
        gr integer,
        last_name text,
        pe integer,
        rubl integer,
        msg_count_1w integer
    );
    """

con = sqlite3.connect(db.file_path)
cur = con.cursor()
cur.execute(sql_create_groups_table)
cur.execute(sql_create_students_table)
cur.execute(f'PRAGMA max_page_count = {db.max_size}')
con.close()

print('`db.sqlite` was created')
