from aiogram import Bot, Dispatcher
import asyncio
import os

from Commands.bot import BotCommandsHandler
from config import envVar
from logger import logger
from utils import getTime

async def main():
    startTime = getTime()

    bot = Bot(token=os.getenv(envKeyToken))
    me = await bot.get_me()
    dp = Dispatcher()

    BotCommandsHandler(bot, dp, me, startTime).registerCommands()

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
