import aiogram
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import qrcode
import io
import os
import random
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
    
@special_router.message(Command(commands=['base', 'сс']))
async def command_base(msg: Message):
    await parse_msg(msg)

    if len(msg.text.split()) < 2:
        await msg.answer(empty_msg)
        return
    arguments = msg.text.split()

    base = arguments[1]
    base_pattern = r'^(\d+)-(\d+)$'
    base_match = re.match(base_pattern, base)
    try:
        base1 = int(base_match.group(1))
        base2 = int(base_match.group(2))
    except:
        await msg.answer(base_bad_base)
        return

    num = arguments[2]
    num_pattern = r'^[0-9A-F]{1,16}$'
    num_match = re.match(num_pattern, num, re.I)
    try:
        num = num_match.group(0).upper()
        num_10 = int(num, base1)
    except:
        await msg.answer(base_bad_num)
        return

    res = ''
    while num_10 > 0:
        digit = num_10 % base2
        if digit > 9:
            digit = chr(digit + 55)
        res = str(digit) + res
        num_10 //= base2

    await msg.answer(
        base_ok.format(num, base1, base2, res),
        parse_mode='HTML')
    
@special_router.message(Command(commands=['math', 'математика']))
async def command_math(msg: Message):
    await parse_msg(msg)

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

@special_router.message(Command(commands=['qr']))
async def command_qr(msg: Message):
    await parse_msg(msg)
    
    if len(msg.text.split()) < 2:
        await msg.answer(empty_msg)
        return
    text = ' '.join(x for x in msg.text.split()[1:])

    qr = qrcode.QRCode(border=1)
    qr.add_data(text)
    qr.make()
    try:
        qr_img = qr.make_image(qr_cant_generate)
    except:
        await msg.answer()
        return
    temp_qr_img_path = get_path(msg.from_user.id, 'png')
    qr_img.save(temp_qr_img_path)

    img = FSInputFile(temp_qr_img_path, filename='qr_code.png')
    await msg.answer_photo(
        photo=img,
        caption=f'{qr_ok}\n{text}'
    )

    os.remove(temp_qr_img_path)

@special_router.message(Command(commands=['random', 'рандом']))
async def command_random(msg: Message):
    await parse_msg(msg)

    if len(msg.text.split()) < 2:
        await msg.answer(empty_msg)
        return
    arguments = msg.text.split()

    scope = arguments[1]
    scope_pattern = r'^(\d{1,8})-(\d{1,8})$'
    scope_match = re.match(scope_pattern, scope)
    try:
        scope_a = int(scope_match.group(1))
        scope_b = int(scope_match.group(2))
        if scope_a > scope_b:
            raise Exception
    except:
        await msg.answer(random_bad_scope)
        return

    try:
        amount = int(arguments[2])
        if not(1 <= amount <= 10):
            raise Exception
    except:
        await msg.answer(random_bad_amount)
        return

    s = ''
    for _ in range(amount):
        s += str(random.randint(scope_a, scope_b)) + '\n'
    s = f'<code>{s}</code>'
    await msg.answer(
        s,
        parse_mode='HTML')

@special_router.message(Command(commands=['yt', 'ютуб', 'ютьуб']))
async def command_yt(msg: Message):
    await parse_msg(msg)

    if len(msg.text.split()) < 2:
        await msg.answer(empty_msg)
        return

    # ПОТЕНЦИАЛЬНО ОПАСНЫЙ КОД
    video_url = shlex.quote(msg.text.split()[1])[1:-1]
    video_url = video_url.replace('youtube.com/watch?v=', 'youtu.be/').split('?')[0]
    video_url_pattern = r'^(https?:\/\/)?(www\.)?(youtu\.be\/)([\w-]+)$'
    if not re.match(video_url_pattern, video_url):
        await msg.answer(yt_bad_url)
        return

    yt_opts = {}
    yt = yt_dlp.YoutubeDL(yt_opts)
    yt_dlp_command = ['yt-dlp', '-g', video_url]
    download_url = subprocess.check_output(yt_dlp_command, shell=False).decode('utf-8').strip()        

    await msg.answer(
        f"{yt_ok}\n<a href='{download_url}'>{yt_download}</a>",
        parse_mode='HTML')
