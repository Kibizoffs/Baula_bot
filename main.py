import aiogram
import asyncio
import os

from config import env_key_token
from logger import logger
from utils import get_time

start_time = get_time()

bot = aiogram.Bot(token=os.getenv(env_key_token))
dp = aiogram.Dispatcher()

if __name__ == '__main__':
    from Commands.bot import bot_router
    from Commands.db import db_router
    from Events.google_docs import google_docs_router
    from Events.send_baula_res import send_baula_res_router
    from Events.stats import stats_router
    from Events.vk import vk_router
    dp.include_routers(
        bot_router, db_router, google_docs_router,
        send_baula_res_router, stats_router, vk_router)

    asyncio.run(dp.start_polling(bot))

