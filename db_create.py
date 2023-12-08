import sqlite3

from config import db

sql_create_groups_table = \
    """
    CREATE TABLE IF NOT EXISTS Groups (
        id integer PRIMARY KEY,
        group_id integer,
        ch_stats integer,
        url_baula text,
        ch_mathhedgehog integer,
        ch_profkomvmk integer
    );
    """
sql_create_students_table = \
    """
    CREATE TABLE IF NOT EXISTS Students (
        id integer PRIMARY KEY,
        last_name text,
        group_id integer,
        pe integer,
        rubl integer,
        msg_count_1w integer,
        send_baula_res integer
    );
    """

con = sqlite3.connect(db.file_path)
cur = con.cursor()
cur.execute(sql_create_groups_table)
cur.execute(sql_create_students_table)
cur.execute(f'PRAGMA max_page_count = {db.max_size}')
con.close()

print('`db.sqlite` was created')
