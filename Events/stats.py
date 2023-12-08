import aiogram
import asyncio
from aiogram.types import Message
from datetime import datetime

from config import db
from main import bot

stats_router = aiogram.Router()

@stats_router.message()
async def parse_msgs(msg: Message):
    student_id = msg.from_user.id
    group_id = ?

    print('D1: ', student_id, ' ', group_id, ' ', msg.text)

    db.cur.execute("SELECT ch_stats FROM Groups WHERE id = ?", (group_id,))
    group_row = db.cur.fetchone()
    if not group_row:
        return
    ch_stats = group_row[0]
    try:
        ch = await bot.get_chat(ch_stats)
    except:
        print(f"{str(group_id)} group doesn't have {str(ch_stats)} channel")
        return

    db.cur.execute("SELECT msg_count_1w FROM Students WHERE id = ?, group_id = ?", (student_id, group_id))
    student_row = db.cur.fetchone()
    if not student_row:
        return
    msg_count_1w = student_row[0]
    if msg_count_1w > 2048:
        return

    db.cur.execute("UPDATE Students SET msg_count_1w = ? WHERE id = ?", (msg_count_1w + 1, student_id,))
    db.con.commit()

@stats_router.message()
async def send_and_clear_stats(msg: Message):
    while True:
        now = datetime.now()
        if now.weekday() == 4 and now.hour == 18 and now.minute == 0:
            db.cur.execute("SELECT id ch_stats FROM Groups")
            group_rows = db.cur.fetchall()
            for group_row in group_rows:
                group_id = group_row[0]
                ch_stats = group_row[1]

                db.cur.execute("SELECT id, msg_count_1w FROM Students WHERE Group = ?", (group_id,))
                student_rows = db.cur.fetchall()
                for student_row in student_rows:
                    student_id = student_row[0]
                    msg_count_1w = student_row[1]
                    group_msg_data = [student_id, msg_count_1w]
                    
                db.cur.execute("UPDATE Students SET msg_count_1w = 0 WHERE msg_count_1w != -1")
                group_msg_data.sort()
                
                answer = '\n'.join(f"@{x[0]}: {x[1] if x[1] < 2048 else 'MAX'}" for x in group_msg_data)
                await bot.send_message(chat=ch_stats, text=answer)

                await asyncio.sleep(7 * 24 * 60 * 60)
        else:
            await asyncio.sleep(60)
