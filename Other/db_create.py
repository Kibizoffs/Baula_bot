import sqlite3

sql_create_groups_table = \
    """
    CREATE TABLE IF NOT EXISTS Groups (
        ID integer PRIMARY KEY,
        ch_stats integer,
        baula_url text,
        ch_repost_mathhedgehog integer,
        ch_repost_profkomvmk integer
    );
    """
sql_create_students_table = \
    """
    CREATE TABLE IF NOT EXISTS Students (
        ID integer PRIMARY KEY,
        last_name text,
        first_name text,
        middle_name text,
        'group' integer,
        show_baula_res integer,
        msg_count_1w integer
    );
    """

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
cur.execute(sql_create_groups_table)
cur.execute(sql_create_students_table)
