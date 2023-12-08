import aiogram
from aiogram.filters import Command
from aiogram.types import \
    Message, ReplyKeyboardMarkup, KeyboardButton
from platform import system

from config import admin_ids
from main import bot, start_time
from messages import *
from utils import *

bot_router = aiogram.Router()

@bot_router.message(Command(commands=['start', 'help', 'старт', 'хелп', 'хэлп', 'помощь']))
async def command_help(msg: Message):
    await msg.answer(help_text)

@bot_router.message(Command(commands=['baula', 'баула']))
async def command_baula(msg: Message):
    current_time = get_time()
    me = await bot.get_me()
    await msg.answer(
        text=baula_txt.format(
            me.id, me.username, aiogram.__version__, system(),
            str(current_time - start_time).split('.')[0]
        ),
        parse_mode='HTML',
        disable_web_page_preview=True
    )

@bot_router.message(Command(commands=['feedback', 'отзыв']))
async def command_feedback(msg: Message):
    if len(msg.text.split()) < 2:
        await msg.answer(empty_msg)
        return
    for admin_id in admin_ids:
        try:
            user = msg.from_user
            username = f'@{user.username}' if user.username else user.id
            await bot.send_message(chat_id=admin_id, text=f'{username}\n{msg.text}')
        except:
            await msg.answer(feedback_err)
            return
    await msg.answer(feedback_ok)
