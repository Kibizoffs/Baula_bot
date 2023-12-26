import aiogram
import asyncio
from aiogram.types import Message
from datetime import datetime, timedelta

from config import *
from main import bot
from logger import logger
from vars import *

messages_router = aiogram.Router()

def count_msg(user_id: int, group_id: int):
    db.cur.execute(f'SELECT {banned_key} FROM Students WHERE {id_key} = ?', (user_id,))
    res = db.cur.fetchone()
    if res and res[0] != None:
        return

    db.cur.execute(f'SELECT {gr_key}, {thread_stats_key} FROM Groups WHERE {id_key} = ?', (group_id,))
    res = db.cur.fetchone()
    if not res or res[1] == None:
        return
    gr = res[0]

    db.cur.execute(f'SELECT {msg_count_1w_key} FROM Students WHERE {id_key} = ? AND {gr_key} = ?', (user_id, gr))
    res = db.cur.fetchone()
    if not res:
        return
    old_msg_count_1w = res[0]
    if old_msg_count_1w == None:
        return

    new_msg_count_1w = old_msg_count_1w + 1
    if new_msg_count_1w > 2048:
        return
    db.cur.execute(f'UPDATE Students SET {msg_count_1w_key} = ? WHERE {id_key} = ?', (new_msg_count_1w, user_id))
    db.con.commit()

@messages_router.message()
async def parse_msg(msg: Message):
    current_time = datetime.now()
    last_friday_18 = current_time.replace(
        hour=stats_hour,
        minute=stats_minute)
    if current_time.weekday() == stats_weekday and current_time.hour >= stats_hour:
        subtract_days = 0
    else:
        subtract_days = last_friday_18.weekday() - stats_weekday if last_friday_18.weekday() >= (stats_weekday + 1) else 7 - (stats_weekday - last_friday_18.weekday())
    last_friday_18 -= timedelta(days=subtract_days)
    if msg.date.timestamp() < last_friday_18.timestamp():
        return 

    user_id = msg.from_user.id
    chat_id = msg.chat.id

    count_msg(user_id, chat_id)

    time_threshold = current_time - timedelta(minutes=1)
    if msg.date.timestamp() < time_threshold.timestamp():
        return
    
    if msg.text.startswith('/'):
        s = (f'\nChat ID: {chat_id}\n' +
        f'Command: {msg.text.split()[0]}\n')
        if chat_id != user_id:
            s += f'User ID: {user_id}\n'

        logger.info(s)

async def send_and_clear_stats():
    while True:
        now = datetime.now()
        if now.weekday() == stats_weekday and now.hour == stats_hour and now.minute == stats_minute:
            db.cur.execute(f"SELECT {', '.join(x for x in [gr_key, id_key, thread_stats_key])} FROM Groups")
            group_rows = db.cur.fetchall()
            for group_row in group_rows:
                gr = group_row[0]
                group_id = group_row[1]
                thread_stats = group_row[2]
                if not thread_stats:
                    return

                db.cur.execute(f"SELECT {', '.join(x for x in [id_key, msg_count_1w_key])} FROM Students WHERE {gr_key} = ?", (gr,))
                student_rows = db.cur.fetchall()
                group_msg_data = []
                for student_row in student_rows:
                    msg_count_1w = student_row[1]
                    if not msg_count_1w:
                        continue
                    try:
                        student = await bot.get_chat_member(group_id, user_id=student_row[0])
                        group_msg_data.append((msg_count_1w, student.user))
                    except:
                        pass

                if len(group_msg_data) < 1:
                    return

                group_msg_data.sort(reverse=True)
                s = 0
                answer = ''
                for member in group_msg_data:
                    user = member[1]
                    if user.username:
                        full_name = f'@{user.username}'
                    else:
                        full_name = user.first_name
                    s += member[0]
                    answer += (full_name + f': {str(member[0])}\n')
                answer = amount_of_msgs.format(str(s)) + answer

                await bot.send_message(
                    chat_id=group_id,
                    message_thread_id=thread_stats,
                    text=answer,
                    parse_mode='HTML')

                db.cur.execute(f'UPDATE Students SET {msg_count_1w_key} = 0 WHERE {gr_key} = {gr}')
                db.con.commit()

                await asyncio.sleep(7 * 24 * 60 * 60)
        else:
            await asyncio.sleep(60)
