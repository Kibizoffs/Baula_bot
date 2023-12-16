import aiogram
from aiogram.filters import Command
from aiogram.types import Message

from Events.messages import parse_msg
from main import bot

admin_router = aiogram.Router()

def is_admin(user_id: int) -> bool:
    db.cur.execute(f'SELECT {admin_key} FROM Students WHERE {id_key} = ?', (user_id,))
    res = db.cur.fetchone()
    if not res or res[0] == None:
        return False
    else:
        return True
    
@admin_router.message(Command(commands=['say', 'сказать']))
async def command_say(msg: Message):
    await parse_msg(msg)

    if not is_admin(msg.from_user.id):
        return
    try:
        await msg.delete()
    except:
        pass
    
    if len(msg.text.split()) < 2:
        await msg.answer(empty_msg)
        return
    await msg.answer(
        text=' '.join(fr'{x}' for x in msg.text.split()[1:]),
        parse_mode='HTML')
