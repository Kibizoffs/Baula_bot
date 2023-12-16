import aiogram
from aiogram.filters import Command
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton)
from platform import system

from Events.messages import parse_msg
from main import bot, start_time
from vars import *
from utils import *

bot_router = aiogram.Router()

@bot_router.message(Command(commands=['start', 'help', 'старт', 'хелп', 'хэлп', 'помощь']))
async def command_help(msg: Message):
    await parse_msg(msg)

    await msg.answer(help_txt)

@bot_router.message(Command(commands=['baula', 'баула']))
async def command_baula(msg: Message):
    await parse_msg(msg)

    current_time = get_time()
    me = await bot.get_me()
    await msg.answer(
        text=baula_txt.format(
            me.id,
            me.username,
            aiogram.__version__,
            system(),
            str(current_time - start_time).split('.')[0]
        ),
        parse_mode='HTML',
        disable_web_page_preview=True
    )

@bot_router.message(Command(commands=['feedback', 'отзыв']))
async def command_feedback(msg: Message):
    await parse_msg(msg)
    
    if len(msg.text.split()) < 2:
        await msg.answer(empty_msg)
        return
    db.cur.execute(f'SELECT {id_key} FROM Students WHERE {admin_key} = ?', (1,))
    res = db.cur.fetchall()
    for admin in res:
        try:
            user = msg.from_user
            name = f'@{user.username}' if user.username else user.id
            admin_id = admin[0]
            await bot.send_message(
                chat_id=admin_id,
                text=(
                    f'{name}:\n'+
                    msg.text
                ),
                parse_mode='HTML')
        except:
            await msg.answer(feedback_err)
            return
    await msg.answer(feedback_ok)
