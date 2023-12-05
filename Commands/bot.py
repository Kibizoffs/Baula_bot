import aiogram
from aiogram.filters import Command
from aiogram.types import \
    Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums.chat_type import ChatType
from platform import system

from config import admin_ids
from main import bot, start_time
from utils import get_time

bot_router = aiogram.Router()

def create_keyboard(keyboard_type: str):
    buttons = []
    match keyboard_type:
        case '!main':
            button_bot = KeyboardButton(text='!bot')
            button_personal = KeyboardButton(text='!personal')
            button_stats = KeyboardButton(text='!stats')
            buttons.extend([[button_bot], [button_personal], [button_stats]])
        case '!bot':
            button_baula = KeyboardButton(text='/baula')
            button_feedback = KeyboardButton(text='/feedback')
            buttons.extend([[button_baula], [button_feedback]])
        case '!personal':
            button_passport = KeyboardButton(text='/passport')
            button_edit = KeyboardButton(text='/edit')
            button_register = KeyboardButton(text='/register')
            button_delete = KeyboardButton(text='/delete')
            buttons.extend([[button_passport], [button_edit], [button_register, button_delete]])
        case '!stats':
            button_stats = KeyboardButton(text='/stats')
            buttons.extend([[button_stats]])
    if keyboard_type != '!main':
        buttons.append([KeyboardButton(text='!back')])
    keyboard = ReplyKeyboardMarkup(keyboard=buttons)
    return keyboard

@bot_router.message(Command(commands=['start', 'help', 'старт', 'хелп', 'хэлп', 'помощь']))
async def command_help(msg: Message):
    if msg.chat.type != ChatType.PRIVATE:
        await msg.answer(text='Вы можете воспользоваться /start только в ЛС')
        return
    await msg.answer(text='Меню команд', reply_markup=create_keyboard('!main'))

@bot_router.message(Command(commands=['baula', 'баула']))
async def command_baula(msg: Message):
    currentTime = get_time()
    me = await bot.get_me()
    await msg.answer(text=\
        f"ID: <code>{me.id}</code>\n" \
        + f"Юзернейм: {me.username}\n"\
        + f"Библиотека: <a href='https://pypi.org/project/aiogram/'>Aiogram {aiogram.__version__}</a>\n" \
        + f"Хостинг: <a href='https://timeweb.cloud/r/kibizoffs1'>Timeweb</a>\n" \
        + f"Платформа: {system()}\n" \
        + f"Время работы: {str(currentTime - start_time).split('.')[0]}\n",
        parse_mode='HTML',
        disable_web_page_preview=True
    )

@bot_router.message(Command(commands=['feedback', 'отзыв']))
async def command_feedback(msg: Message):
    if msg.chat.type != ChatType.PRIVATE:
        await msg.answer('Вы можете воспользоваться /register только в ЛС')
        return
    if len(msg.text.split()) < 2:
        await msg.answer('Ваше сообщение пустое')
        return
    for admin_id in admin_ids:
        try:
            await bot.send_message(chat_id=admin_id, text=f'{msg.from_user.username}\n{msg.text}')
        except Exception as e:
            await msg.answer('Ваше сообщение не было доставлено до администрации')
            print(f"Не получилось отправить сообщение админу с ID: {admin_id}. Ошибка: {e}")
            return
    await msg.answer('Ваше сообщение было успешно отправлено администрации')

@bot_router.message()
async def button_click(msg: Message):
    if msg.text.startswith('!'):
        match msg.text:
            case '!back':
                await msg.answer(text='Меню команд', reply_markup=create_keyboard('!main'))
            case '!bot':
                await msg.answer(text="Раздел команд 'бот'", reply_markup=create_keyboard('!bot'))
            case '!personal':
                await msg.answer(text="Раздел команд 'личное'", reply_markup=create_keyboard('!personal'))
            case '!stats':
                await msg.answer(text="Раздел команд 'статистика'", reply_markup=create_keyboard('!stats'))
