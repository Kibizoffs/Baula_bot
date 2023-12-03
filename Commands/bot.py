import aiogram
from aiogram import types
from aiogram.filters import Command
from platform import system

from utils import getTime

class BotCommandsHandler:
    def __init__(self, bot, dp, me, startTime):
        self.bot = bot
        self.dp = dp
        self.me = None

    async def commandHelp(self, msg: types.message):
        currentTime = getTime()
        await msg.answer(text="Ты обречён")

    async def commandBot(self, msg: types.message):
        currentTime = getTime()
        await msg.answer(
            text=f"User: {self.me.mention}\nID: {self.me.id}\n" \
                + f"Library: <a href='https://pypi.org/project/aiogram/'>Aiogram {aiogram.__version__}</a>\n" \
                + f"Host: <a href='https://timeweb.cloud/r/kibizoffs1'>Timeweb</a>\n" \
                + f"Platform: {system()}\n" \
                + f"Uptime: {currentTime - startTime}\n"
        )
    
    def registerCommands(self):
        self.dp.message.register(self.commandHelp, Command(commands=['help', 'start', 'старт', 'помощь', 'хелп', 'хэлп']))
        self.dp.message.register(self.commandBot, Command(commands=['bot', 'бот']))
