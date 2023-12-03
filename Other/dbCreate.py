import sqlite3

sqlCreateTable = \
    """
    CREATE TABLE IF NOT EXISTS Students (
        tgUsername text PRIMARY KEY,
        studentID text,
        lastName text,
        middleName text,
        firstName text,
        'group' integer,
        showResults integer
    );
    """

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
cur.execute(sqlCreateTable)
