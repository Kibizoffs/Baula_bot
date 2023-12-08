import aiogram
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

import qrcode
import io
import os
from PIL import Image, ImageDraw, ImageFont

from config import get_path
from main import bot
from messages import *

special_router = aiogram.Router()

@special_router.message(Command(commands=['qr']))
async def command_qr(msg: Message):
    if len(msg.text.split()) < 2:
        await bot.send_message(empty_message)
        return

    text = ' '.join(x for x in msg.text.split()[1:])

    qr = qrcode.QRCode(border=1)
    qr.add_data(text)
    qr.make()
    qr_img = qr.make_image()
    qr_img_path = get_path(msg.from_user.id)
    qr_img.save(qr_image_path)
    img = FSInputFile(qr_image_path, filename='qr_code.png')

    await msg.answer_photo(
        photo=img,
        caption=f'QR-код по запросу:\n{text}'
    )

    os.remove(qr_image_path)
