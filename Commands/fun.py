import aiogram
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from PIL import Image, ImageDraw, ImageFont
import random

from config import get_path
from main import bot
from messages import *

fun_router = aiogram.Router()

@fun_router.message(Command(commands=['hack', 'хак', 'взлом']))
async def command_hack(msg: Message):
    ...

def tameFrames(self, pat_img):
    hand_frames = [
        Image.open(f"Media/Hand/frame{i+1}.png")
        for i in range(5)]
    x = 50
    y = 75
    width = 200
    height = 200
    squish_y_amp = 10
    shake_x_amp = 4
    shake_y_amp = 4
    c = 5
    frames = []
    for i in range(c):
        frame = Image.new("RGBA", (256, 256), (54, 57, 62, 1))
        squish_y = int(squish_y_amp * cos(2 * pi / c * i))
        squish_x = width * height // (squish_y + height) - width
        shake_x = int(shake_x_amp * sin(2 * pi / c * i))
        shake_y = int(shake_y_amp * -cos(2 * pi / c * i))
        tame_coords = (x - squish_x // 2 + shake_x, y - squish_y + shake_y)
        frame.paste(
            pat_img.resize((squish_x + width, squish_y + height)),
            pat_coords,
        )
        hand = hand_frames[6 * i // c]
        frame.paste(hand, (shake_x, shake_y), hand)
        frames.append(frame)
    return frames

@fun_router.message(Command(commands=['pat', 'похвалить']))
async def command_pat(msg: Message):
    avas = await bot.get_user_profile_photos(author.id)
    ava_id = avas.photos[0][0].file_id
    ava = await bot.get_file(ava_id)
    temp_png_path = f'Temp/{str(author.id)}.png'
    await bot.download_file(ava.file_path, temp_png_path)
    ava = Image.open(temp_png_path)
    ava = ava.resize((256, 256))
    frames = pat_frames(ava)
    frames[0].save(
        buffer_output,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0,
        optimize=True)
    img.paste(ava, (72, 75))
    img.save(get_path(msg.from_user.id))
    img = FSInputFile(temp_png_path, filename='trash.png')

    await msg.answer_photo(photo=img)

    os.remove(temp_png_path)

@fun_router.message(Command(commands=['stick', 'палка']))
async def command_stick(msg: Message):
    stick = random.choice(['У тебя False', '0' + '=' * random.randint(5,20) + 'D'])
    await msg.answer(stick)

@fun_router.message(Command(commands=['trash', 'мусор']))
async def command_trash(msg: Message):
    author = msg.from_user
    img = Image.open('Media/trash.jpg')
    img_draw = ImageDraw.Draw(img)
    img_font = ImageFont.truetype("Fonts/arial.ttf", 18)
    img_draw.text(
        (240, 105),
        f'{author.username}.exe\n' +
        f"Память: {random.randint(1, 1023)}{random.choice(['kB', 'MB'])}",
        font=img_font,
        fill=(0, 0, 0))
    avas = await bot.get_user_profile_photos(author.id)
    ava_id = avas.photos[0][0].file_id
    ava = await bot.get_file(ava_id)
    temp_png_path = f'Temp/{str(author.id)}.png'
    await bot.download_file(ava.file_path, temp_png_path)
    ava = Image.open(temp_png_path)
    ava = ava.resize((128, 128))
    img.paste(ava, (72, 75))
    img.save(get_path(msg.from_user.id))
    img = FSInputFile(temp_png_path, filename='trash.png')

    await msg.answer_photo(photo=img)

    os.remove(temp_png_path)

@fun_router.message(Command(commands=['sal', 'salnikov', 'сал', 'сальников']))
async def command_sal(msg: Message):
    author = msg.from_user
    img = Image.open('Media/sal.jpg')
    img_draw = ImageDraw.Draw(img)
    img_font = ImageFont.truetype("Fonts/arial.ttf", 18)
    avas = await bot.get_user_profile_photos(author.id)
    ava_id = avas.photos[0][0].file_id
    ava = await bot.get_file(ava_id)
    temp_png_path = f'Temp/{str(author.id)}.png'
    await bot.download_file(ava.file_path, temp_png_path)
    ava = Image.open(temp_png_path)
    ava = ava.resize((256, 256))
    img.paste(ava, (256, 0))
    img.save(get_path(msg.from_user.id))
    img = FSInputFile(temp_png_path, filename='salnikov.png')

    await msg.answer_photo(photo=img)

    os.remove(temp_png_path)

'''
@fun_router.message(Command(commands=['zachet', 'зачёт']))
async def command_zachet(msg: Message):
    ...
'''
