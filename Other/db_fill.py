import sqlite3

sql_fill_groups_table = \
    """
    INSERT INTO Groups (
        id,
        gr,
        thread_stats,
        thread_mathhedgehog,
        thread_profkomvmk,
        url_baula
    ) 
    VALUES (
        -1001922535101,
        107,
        18064,
        5850,
        5850,
        '1gR7o0t9ewkMb499jHVt-z36Fgd8erb0y-blv_Rv6Kz0'
    );
    """

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
cur.execute(sql_fill_groups_table)
con.commit()
con.close()

print('`db.sqlite` обновлён')
