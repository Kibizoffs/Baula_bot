import aiogram
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from math import pi, sin, cos
import os
from PIL import Image, ImageDraw, ImageFont
import random

from Events.messages import parse_msg
from main import bot
from utils import *
from vars import *

fun_router = aiogram.Router()

def hand_frames(ava):
    x = 50
    y = 75
    width = 200
    height = 200
    squish_y_amp = 10
    shake_x_amp = 4
    shake_y_amp = 4
    c = 4
    hand_frames = [
        Image.open(path_hand.format(str(i+1))) for i in range(4)]
    frames = []
    for i in range(c):
        frame = Image.new("RGBA", (256, 256), (0, 0, 0, 1))
        squish_y = int(squish_y_amp * cos(2 * pi / c * i))
        squish_x = width * height // (squish_y + height) - width
        shake_x = int(shake_x_amp * sin(2 * pi / c * i))
        shake_y = int(shake_y_amp * -cos(2 * pi / c * i))
        hand_coords = (x - squish_x // 2 + shake_x, y - squish_y + shake_y)
        frame.paste(
            ava.resize((squish_x + width, squish_y + height)),
            hand_coords,
        )
        hand = hand_frames[(c + 1) * i // c]
        frame.paste(hand, (shake_x, shake_y), hand)
        frames.append(frame)
    return frames

@fun_router.message(Command(commands=['hand', 'рука']))
async def command_hand(msg: Message):
    if len(msg.text.split()) > 1:
        user_id = msg.text.split()[1]
        try:
            user = (await bot.get_chat_member(msg.chat.id, user_id=user_id)).user
        except:
            await msg.answer(trash_no_user)
            return
    else:
        user = msg.from_user

    avas = await bot.get_user_profile_photos(user.id)
    if len(avas.photos) < 1:
        await msg.answer(no_profile_photo)
        return
    ava_id = avas.photos[0][0].file_id
    ava = await bot.get_file(ava_id)
    temp_png_path = get_path(user.id, 'png')
    await bot.download_file(ava.file_path, temp_png_path)
    ava = Image.open(temp_png_path)
    ava = ava.resize((256, 256))
    frames = hand_frames(ava)
    temp_gif_path = get_path(user.id, 'gif')
    frames[0].save(
        temp_gif_path,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=60)
    gif = FSInputFile(path=temp_gif_path, filename=filename_hand)

    await msg.answer_animation(gif)

    os.remove(temp_png_path)
    os.remove(temp_gif_path)


async def sal_get_photos(user, i, img):
    temp_png_path = get_path(user.id, 'png')
    avas = await bot.get_user_profile_photos(user.id)
    if len(avas.photos) < 1:
        await msg.answer(no_profile_photo)
        return
    ava_id = avas.photos[0][0].file_id
    ava = await bot.get_file(ava_id)
    await bot.download_file(ava.file_path, temp_png_path)
    ava = Image.open(temp_png_path)
    ava = ava.resize((128, 128))
    if i == 1:
        img.paste(ava, (128, 0))
    elif i == 2:
        img.paste(ava, (128, 128))
    ava.close()
    os.remove(temp_png_path)
    return img

@fun_router.message(Command(commands=['sal', 'salnikov', 'сал', 'сальников']))
async def command_sal(msg: Message):
    args = msg.text.split()

    if len(args) < 3:
        await msg.answer(sal_2_arguments)
        return
    user1_id = args[1]
    user2_id = args[2]
    try:
        user1 = (await bot.get_chat_member(msg.chat.id, user_id=user1_id)).user
        user2 = (await bot.get_chat_member(msg.chat.id, user_id=user2_id)).user
    except:
        await msg.answer(sal_2_arguments)
        return

    img = Image.open(path_salnikov)
    img = await sal_get_photos(user1, 1, img)
    img = await sal_get_photos(user2, 2, img)

    temp_png_path = get_path(f'{user1.id}_{user2.id}', 'png')
    img.save(temp_png_path)
    
    img = FSInputFile(temp_png_path, filename=filename_salnikov)
    await msg.answer_photo(photo=img)

    os.remove(temp_png_path)


@fun_router.message(Command(commands=['trash', 'мусор']))
async def command_trash(msg: Message):
    if len(msg.text.split()) > 1:
        user_id = msg.text.split()[1]
        try:
            user = (await bot.get_chat_member(msg.chat.id, user_id=user_id)).user
        except:
            await msg.answer(trash_no_user)
            return
    else:
        user = msg.from_user

    img = Image.open(path_trash)
    img_draw = ImageDraw.Draw(img)
    img_font = ImageFont.truetype("Fonts/arial.ttf", 18)
    img_draw.text(
        (240, 105),
        f'{user.username}.exe\n' +
        f"{trash_memory} {random.randint(1, 1023)}{random.choice(['kB', 'MB'])}",
        font=img_font,
        fill=(0, 0, 0)
    )

    avas = await bot.get_user_profile_photos(user.id)
    if len(avas.photos) < 1:
        await msg.answer(no_profile_photo)
        return
    ava_id = avas.photos[0][0].file_id
    ava = await bot.get_file(ava_id)
    temp_png_path = get_path(user.id, 'png')
    await bot.download_file(ava.file_path, temp_png_path)
    ava = Image.open(temp_png_path)
    ava = ava.resize((128, 128))
    img.paste(ava, (72, 75))
    img.save(temp_png_path)
    img = FSInputFile(temp_png_path, filename=filename_hand)

    await msg.answer_photo(photo=img, caption=trash_text)

    os.remove(temp_png_path)
