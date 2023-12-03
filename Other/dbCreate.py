# библиотеки
import sqlite3
# модули
from config import *

sqlCreateTable = \
    """
    CREATE TABLE IF NOT EXISTS STUDENTS (
        username text,
        lastName text,
        middleName text,
        firstName text,
        'group' integer
    );
    """

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
cur.execute(sqlCreateTable)
