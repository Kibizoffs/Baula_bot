import sqlite3

sqlCreateGroupsTable = \
    """
    CREATE TABLE IF NOT EXISTS Groups (
        ID integer PRIMARY KEY,
        ch_stats integer,
        ch_repost_mathhedgehog integer,
        ch_repost_profkomvmk integer
    );
    """
sqlCreateStudentsTable = \
    """
    CREATE TABLE IF NOT EXISTS Students (
        tg_username text PRIMARY KEY,
        last_name text,
        middle_name text,
        first_name text,
        'group' integer,
        show_baula_results integer
    );
    """

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
cur.execute(sqlCreateGroupsTable)
cur.execute(sqlCreateStudentsTable)
