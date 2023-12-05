import sqlite3

from config import db

sql_create_groups_table = \
    """
    CREATE TABLE IF NOT EXISTS Groups (
        ID integer PRIMARY KEY,
        ch_stats integer,
        url_baula text,
        ch_mathhedgehog integer,
        ch_profkomvmk integer
    );
    """
sql_create_students_table = \
    """
    CREATE TABLE IF NOT EXISTS Students (
        ID integer PRIMARY KEY,
        last_name text,
        first_name text,
        middle_name text,
        group_id integer,
        send_baula_res integer,
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
