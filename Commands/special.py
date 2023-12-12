import aiogram
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import json
import qrcode
import io
import os
import re
import shlex
import subprocess
from sympy import solve, sympify
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import quote
import yt_dlp

from Events.messages import parse_msg
from main import bot
from utils import *
from vars import *

special_router = aiogram.Router()

@special_router.message(Command(commands=['qr']))
async def command_qr(msg: Message):
    if len(msg.text.split()) < 2:
        await msg.answer(empty_msg)
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

    os.remove(temp_qr_img_path)

@special_router.message(Command(commands=['yt', 'ютуб', 'ютьуб']))
async def command_yt(msg: Message):
    if len(msg.text.split()) < 2:
        await msg.answer(empty_msg)
        return

    # ПОТЕНЦИАЛЬНО ОПАСНЫЙ КОД. ТРЕБУЕТСЯ МАКСИМУМ ЗАЩИТЫ
    video_url = shlex.quote(msg.text.split()[1])[1:-1]
    video_url = video_url.replace('youtube.com/watch?v=', 'youtu.be/').split('?')[0]
    regex_url = r'^(https?:\/\/)?(www\.)?(youtu\.be\/)([\w-]+)$'
    if not re.match(regex_url, video_url):
        await msg.answer(yt_bad_url)
        return

    yt_opts = {}
    yt = yt_dlp.YoutubeDL(yt_opts)
    yt_dlp_command = ['yt-dlp', '-g', video_url]
    download_url = subprocess.check_output(yt_dlp_command, shell=False).decode('utf-8').strip()        

    await msg.answer(f"{yt_ok}\n<a href='{download_url}'>{yt_download}</a>", parse_mode='HTML')

@special_router.message(Command(commands=['math', 'математика']))
async def command_math(msg: Message):
    if len(msg.text.split()) < 2:
        await msg.answer(empty_msg)
        return
    expression = ' '.join(x for x in msg.text.split()[1:])
    if expression == '':
        await msg.answer(empty_msg)
        return

    try:
        result = sympify(expression).evalf()
    except Exception:
        await msg.answer(math_cant_parse)
        return
    url = 'https://www.wolframalpha.com/input?i=' + quote(expression)
    await msg.answer(
        text=math_result.format(result, url),
        parse_mode='HTML',
        disable_web_page_preview=True)
