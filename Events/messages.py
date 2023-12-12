import aiogram
import asyncio
from aiogram.types import Message
from datetime import datetime, timedelta

from config import db
from main import bot
from vars import *

messages_router = aiogram.Router()

@messages_router.message()
async def parse_msg(msg: Message):
    time_threshold = datetime.now() - timedelta(minutes=1)
    if msg.date.timestamp() < time_threshold.timestamp():
        return

    user_id = msg.from_user.id
    group_id = msg.chat.id

    db.cur.execute("SELECT gr, thread_stats FROM Groups WHERE id = ?", (group_id,))
    res = db.cur.fetchone()
    if not res or res[1] == None:
        return
    gr = res[0]

    db.cur.execute("SELECT msg_count_1w FROM Students WHERE id = ? AND gr = ?", (user_id, gr))
    res = db.cur.fetchone()
    if not res:
        return
    old_msg_count_1w = res[0]
    if old_msg_count_1w == None:
        return

    new_msg_count_1w = old_msg_count_1w + 1
    if new_msg_count_1w > 2048:
        return
    db.cur.execute("UPDATE Students SET msg_count_1w = ? WHERE id = ?", (new_msg_count_1w, user_id))
    db.con.commit()

async def send_and_clear_stats():
    while True:
        now = datetime.now()
        if now.weekday() == 4 and now.hour == 18 and now.minute == 0:
            db.cur.execute("SELECT gr, id, thread_stats FROM Groups")
            group_rows = db.cur.fetchall()
            for group_row in group_rows:
                gr = group_row[0]
                group_id = group_row[1]
                thread_stats = group_row[2]
                if not thread_stats:
                    return

                db.cur.execute("SELECT id, msg_count_1w FROM Students WHERE gr = ?", (gr,))
                student_rows = db.cur.fetchall()
                group_msg_data = []
                for student_row in student_rows:
                    msg_count_1w = student_row[1]
                    if msg_count_1w == None:
                        continue
                    try:
                        student = await bot.get_chat_member(group_id, user_id=student_row[0])
                        group_msg_data.append((msg_count_1w, student.user))
                    except:
                        pass

                if len(group_msg_data) < 1:
                    return

                group_msg_data.sort()
                s = 0
                answer = ''
                for member in group_msg_data:
                    user = x[1]
                    if user.username:
                        full_name = f'@{user.username}'
                    else:
                        full_name = user.first_name
                    s += x[0]
                    answer += (full_name + f': {str(x[0])}\n')
                answer = amount_of_msgs.format(str(s)) + answer

                await bot.send_message(chat_id=group_id, message_thread_id=thread_stats, text=answer)

                db.cur.execute(f'UPDATE Students SET msg_count_1w = 0 WHERE gr = {gr} AND msg_count_1w != NULL')
                db.con.commit()

                await asyncio.sleep(7 * 24 * 60 * 60)
        else:
            await asyncio.sleep(60)
