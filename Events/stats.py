import aiogram
import asyncio
from datetime import datetime

from config import db
from main import bot

stats_router = aiogram.Router()

@stats_router.message()
async def send_and_clear_stats():
    while True:
        now = datetime.now()
        if now.weekday() == 4 and now.hour == 18 and now.minute == 0:

            db.cur.execute("SELECT ID ch_stats FROM Groups")
            group_rows = db.cur.fetchall()
            for group_row in group_rows:
                group_id = group_row[0]
                ch_stats = group_row[1]

                db.cur.execute("SELECT ID, msg_count_1w FROM Students WHERE Group = ?", (group_id,))
                student_rows = db.cur.fetchall()
                for student_row in student_rows:
                    student_id = student_row[0]
                    msg_count_1w = student_row[1]
                    group_msg_data = [msg_count_1w, student_id]
                    
                db.cur.execute("UPDATE Students SET msg_count_1w = 0")
                group_msg_data.sort()
                
                answer = '\n'.join(f'@{x[0]: x[1]}' for x in group_msg_data)
                await bot.send_message(chat=ch_stats, text=answer)

                await asyncio.sleep(7 * 24 * 60 * 60)
        else:
            await asyncio.sleep(60)
