import aiogram
from aiogram.filters import Command
from aiogram.types import \
    Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums.chat_type import ChatType
from platform import system

from config import admin_ids
from main import bot, start_time
from messages import *
from utils import get_time

bot_router = aiogram.Router()

@bot_router.message(Command(commands=['start', 'help', 'старт', 'хелп', 'хэлп', 'помощь']))
async def command_help(msg: Message):
    await msg.answer(help_text)

@bot_router.message(Command(commands=['baula', 'баула']))
async def command_baula(msg: Message):
    currentTime = get_time()
    me = await bot.get_me()
    await msg.answer(
        text=baula_text.format(
            me.id, me.username, aiogram.__version__, system(),
            str(currentTime - start_time).split('.')[0]
        ),
        parse_mode='HTML',
        disable_web_page_preview=True
    )

@bot_router.message(Command(commands=['feedback', 'отзыв']))
async def command_feedback(msg: Message):
    if len(msg.text.split()) < 2:
        await msg.answer(empty_message)
        return
    for admin_id in admin_ids:
        try:
            await bot.send_message(chat_id=admin_id, text=f'{msg.from_user.username}\n{msg.text}')
        except Exception:
            await msg.answer(feedback_err)
            return
    await msg.answer(feedback_ok)
