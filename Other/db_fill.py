import sqlite3

sql_fill_groups_table = \
    """
    INSERT INTO Groups (
        id,
        ch_stats,
        url_baula,
        ch_mathhedgehog,
        ch_profkomvmk 
    ) 
    VALUES (
        1922535101,
        18064,
        '1gR7o0t9ewkMb499jHVt-z36Fgd8erb0y-blv_Rv6Kz0',
        5850,
        5850
    );
    """

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
cur.execute(sql_fill_groups_table)
con.commit()
con.close()

print('`db.sqlite` обновлён')
