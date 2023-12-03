# стандартные модули
import datetime
import aiogram
import logging
from logging import handlers
import os
import platform

UptimeStart = datetime.datetime.utcnow()

async def main():
    bot = Bot(token=os.getenv('password_baula_bot'))
    me = await bot.get_me()
    dp = Dispatcher()
    await dp.start_polling(bot)

@dp.message_handler(commands=['bot'])
async def botInfo():
    uptime = (datetime.datetime.strptime(str(datetime.datetime.utcnow()).split('.')[0], "%Y-%m-%d %H:%M:%S")) - (datetime.datetime.strptime(str(uptimestart1).split('.')[0], "%Y-%m-%d %H:%M:%S"))
    await bot.send_chat_action(author.id, aiogram.types.ChatActions.TYPING)
    await bot.send_message(
        chat_id=author.id,
        text=f"User: {me.mention}\nID: {me.id}\n" \
            + "Library: <a href='https://pypi.org/project/aiogram/'>aiogram {aiogram.__version__}</a>\n" \
            + "Host: <a href='https://contabo.com/en/'>Contabo</a>\n" \
            + "Platform: {me.mention}\n" \
            + "Uptime: {uptime}\n"
    )

if __name__ == '__main__':
    main()
    loaded_time = \
        (datetime.datetime.strptime(str(datetime.datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f')) \
        - (datetime.datetime.strptime(str(uptimestart1), '%Y-%m-%d %H:%M:%S.%f'))
    logger.info(
        f"{bot.get_me().info.username} is online\n" +
        "Loaded in {loaded_time}")
