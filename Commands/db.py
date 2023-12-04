import aiogram
from aiogram.filters import Command
from aiogram.types import Message

from main import bot

db_router = aiogram.Router()

@db_router.message(Command(commands=['passport', 'me', 'паспорт', 'я']))
async def commandPassport(msg: Message):
    await msg.answer(text=\
        f"username: {0}" +\
        f"last_name: {0}" +\
        f"middle_name: {0}" +\
        f"first_name: {0}" +\
        f"group: {0}"+\
        f"show_baula_results: {0}"
    )

@db_router.message(Command(commands=['edit', 'изменить']))
async def commandEdit(msg: Message):
    print('soon')

@db_router.message(Command(commands=['register', 'create', 'создать']))
async def commandRegister(msg: Message):
    print('soon')

@db_router.message(Command(commands=['delete', 'remove', 'удалить']))
async def commandDelete(msg: Message):
    print('soon')
