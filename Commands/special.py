import aiogram
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import json
import qrcode
import io
import os
import re
import subprocess
import shlex
from PIL import Image, ImageDraw, ImageFont
import yt_dlp

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
    temp_qr_img_path = get_path(msg.from_user.id, 'png')
    qr_img.save(temp_qr_img_path)
    img = FSInputFile(temp_qr_img_path, filename='qr_code.png')

    await msg.answer_photo(
        photo=img,
        caption=f'{qr_ok}\n{text}'
    )

    os.remove(qr_image_path)

@special_router.message(Command(commands=['yt', 'ютуб']))
async def command_yt(msg: Message):
    if len(msg.text.split()) < 2:
        await bot.send_message(empty_message)
        return

    yt_opts = {}
    yt = yt_dlp.YoutubeDL(yt_opts)

    video_url = shlex.quote(msg.text.split()[1].split('?')[0])
    print(video_url)
    regex_url = r'^(https?:\/\/)?(www\.)?((youtube\.com\/watch\?v=)|(youtu\.be\/))([\w-]+)$'
    res = re.match(regex_url, video_url)
    if not re.match(regex_url, video_url):
        await msg.answer(yt_bad_url)
        return

    yt_dlp_command = ['yt-dlp', '-g', video_url]
    download_url = subprocess.check_output(yt_dlp_command, shell=False, stdout=subprocess.DEVNULL).decode('utf-8').strip()        

    await msg.answer(f"{yt_ok}\n<a href='{download_url}'>Скачать</a>", parse_mode='HTML')
