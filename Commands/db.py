import aiogram
from aiogram.filters import Command
from aiogram.types import Message

from main import bot

db_router = aiogram.Router()

@db_router.message(Command(commands=['passport', 'me', 'паспорт', 'я']))
async def commandPassport(msg: Message):
    await msg.answer(text=\
        f"username: {msg.author.id}" +\
        f"last_name: {msg.author.id}" +\
        f"middle_name: {msg.author.id}" +\
        f"first_name: {msg.author.id}" +\
        f"group: {msg.author.id}"+\
        f"show_baula_results: {msg.author.id}"
    )

@db_router.message(Command(commands=['register', 'create', 'создать']))
async def commandRegister(msg: Message):
    print('soon')

@db_router.message(Command(commands=['delete', 'remove', 'удалить']))
async def commandDelete(msg: Message):
    print('soon')

@db_router.message(Command(commands=['edit', 'изменить']))
async def commandEdit(msg: Message):
    print('soon')
