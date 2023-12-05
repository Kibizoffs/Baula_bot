import aiogram
import httpx

from main import bot

send_baula_res_router = aiogram.Router()

@send_baula_res_router.message()
async def send_message():
    while True:
        now = datetime.now()

        if now.hour == 18 or now.weekday() == 0 and now.hour in [9, 10, 11, 12, 13, 14, 15]:
            
            await asyncio.sleep(7 * 24 * 60 * 60)
        else:
            await asyncio.sleep(60)
