from datetime import datetime

from config import db

def get_time():
    return datetime.strptime(str(datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f')

def get_group_info(group_id: int):
    con = sqlite3.connect(db.file_path)
    cur = con.cursor()

    select_query = """
        SELECT ID, ch_stats, ch_repost_mathhedgehog, ch_repost_profkomvmk
        FROM Groups
        WHERE ID = ?
    """
    cur.execute(select_query, (group_id,))
    group_data = cur.fetchone()

    con.close()
    return group_data

def get_student_info(tg_username: str):
    con = sqlite3.connect(db.file_path)
    cur = con.cursor()

    select_query = """
        SELECT tg_username, last_name, middle_name, first_name, 'group', show_baula_res
        FROM Students
        WHERE tg_username = ?
    """
    cur.execute(select_query, (tg_username,))
    student_data = cur.fetchone()

    con.close()
    return student_data
