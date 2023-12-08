import aiogram
import asyncio
from aiogram.types import Message
from datetime import datetime

from config import db
from main import bot
from messages import *

stats_router = aiogram.Router()

@stats_router.message()
async def parse_msgs(msg: Message):
    student_id = msg.from_user.id
    group_id = msg.chat.id

    db.cur.execute("SELECT gr, thread_stats FROM Groups WHERE id = ?", (group_id,))
    group_row = db.cur.fetchone()
    if not group_row or not group_row[1]:
        return
    gr = group_row[0]

    db.cur.execute("SELECT msg_count_1w FROM Students WHERE id = ? AND gr = ?", (student_id, gr))
    student_row = db.cur.fetchone()
    if not student_row:
        return
    old_msg_count_1w = student_row[0]

    new_msg_count_1w = old_msg_count_1w + 1
    if new_msg_count_1w > 2048:
        return
    db.cur.execute("UPDATE Students SET msg_count_1w = ? WHERE id = ?", (new_msg_count_1w, student_id))
    db.con.commit()

async def send_and_clear_stats():
    while True:
        now = datetime.now()
        if now.weekday() == 4 and now.hour == 18 and now.minute == 00:
            db.cur.execute("SELECT id, gr, thread_stats FROM Groups")
            group_rows = db.cur.fetchall()
            for group_row in group_rows:
                group_id = group_row[0]
                gr = group_row[1]
                thread_stats = group_row[2]
                if not thread_stats:
                    return

                db.cur.execute("SELECT id, msg_count_1w FROM Students WHERE gr = ?", (gr,))
                student_rows = db.cur.fetchall()
                group_msg_data = []
                for student_row in student_rows:
                    msg_count_1w = student_row[1]
                    student = await bot.get_chat(student_row[0])
                    if msg_count_1w > 0:
                        group_msg_data.append((msg_count_1w, student))
                    
                db.cur.execute("UPDATE Students SET msg_count_1w = 0 WHERE msg_count_1w != -1")

                if len(group_msg_data) < 1:
                    await bot.send_message(chat_id=group_id, message_thread_id=thread_stats, text=no_msgs)
                    return
                group_msg_data.sort()
                
                full_name = f'{student.first_name} {student.last_name}' if student.last_name else student.first_name
                answer = (amount_of_msgs +
                    '\n'.join(f"{full_name}: {x[0] if x[0] < 2048 else 'MAX'}" for x in group_msg_data))
                await bot.send_message(chat_id=group_id, message_thread_id=thread_stats, text=answer)

                await asyncio.sleep(7 * 24 * 60 * 60)
        else:
            await asyncio.sleep(60)

asyncio.run(send_and_clear_stats())
