import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
# изменения
con.commit()
con.close()

print('`db.sqlite` обновлён')
