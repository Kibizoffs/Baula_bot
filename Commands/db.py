import aiogram
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import re

from config import db
from main import bot
from messages import *

db_router = aiogram.Router()

@db_router.message(Command(commands=['passport', 'me', 'паспорт', 'я']))
async def command_passport(msg: Message):
    student_id = msg.from_user.id
    select_columns = [
        'id', 'gr', 'last_name',
        'pe', 'rubl', 'msg_count_1w'
    ]
    db.cur.execute(f"SELECT {', '.join(x for x in select_columns)} FROM Students WHERE id = ?", (student_id,))
    row = db.cur.fetchone()
    if not row:
        msg.answer(not_yet_registered)
        return
    answer = '\n'.join(f'{str(select_columns[i])}: {str(row[i])}' for i in range(len(select_columns)))
    await msg.answer(answer)

@db_router.message(Command(commands=['edit', 'изменить']))
async def command_edit(msg: Message):
    arguments = msg.text.split()
    if len(arguments) < 2:
        await msg.answer(edit_txt, parse_mode='HTML')
        return
    key = arguments[1].lower()
    val = arguments[2]
    if len(val) > 16:
        await msg.answer(too_long_message)
        return
        
    student_id = msg.from_user.id
    select_columns = [
        'id', 'gr', 'last_name',
        'msg_count_1w'
    ]
    db.cur.execute(f"SELECT {', '.join(x for x in select_columns)} FROM Students WHERE id = ?", (student_id,))
    result = db.cur.fetchone()
    if not result:
        await msg.answer(not_yet_registered)
        return

    found = False
    for x in select_columns:
        if x == key:
            found = True
            if val == '':
                dr.cur.execute(f'DELETE FROM Students WHERE id = ? AND {key} = ?')
                await msg.answer(edit_deleted)
            else:
                regex_gr = r'^\d{3}$'
                regex_msg_count_1w = r'^-1|0$'
                if key == 'gr' and (not re.match(regex_gr, val)) or \
                    key == 'msg_count_1w' and (not re.match(regex_msg_count_1w, val)):
                    await msg.answer(wrong_format)
                    return
                db.cur.execute(f'UPDATE Students SET {key} = ? WHERE id = ?', (val, student_id))
                db.con.commit()
                await msg.answer(edit_updated)
            break
    if not found:
        await msg.answer(edit_key_not_found)
        return

@db_router.message(Command(commands=['register', 'create', 'создать']))
async def command_register(msg: Message):
    student_id = msg.from_user.id
    db.cur.execute("SELECT * FROM Students WHERE id = ?", (student_id,))
    result = db.cur.fetchone()
    if result:
        await msg.answer(already_registered)
        return
    db.cur.execute("INSERT INTO Students (id, gr, pe, rubl, msg_count_1w) VALUES (?, ?, ?, ?, ?)",
        (student_id, None, 0, 0, 0))
    db.con.commit()
    await msg.answer(register_ok)
    await msg.answer(edit_txt, parse_mode='HTML')


@db_router.message(Command(commands=['delete', 'remove', 'удалить']))
async def command_delete(msg: Message):
    student_id = msg.from_user.id
    db.cur.execute("SELECT * FROM Students WHERE id = ?", (student_id,))
    result = db.cur.fetchone()
    if not result:
        await msg.answer(not_yet_registered)
        return

    cancel_button = InlineKeyboardButton(text="❌", callback_data="cancel_deletion")
    confirm_button = InlineKeyboardButton(text="✅", callback_data="confirm_deletion")
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_button, confirm_button]])

    await msg.answer(delete_confirm, reply_markup=confirm_keyboard)

@db_router.callback_query()
async def confirm_deletion(query: CallbackQuery):
    student_id = query.from_user.id
    if student_id != query.from_user.id:
        return
    elif query.data == 'cancel_deletion':
        await query.message.answer(delete_cancelled)
    elif query.data == 'confirm_deletion':
        db.cur.execute("DELETE FROM Students WHERE id = ?", (student_id,))
        db.con.commit()
        await query.message.answer(delete_ok)
    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[[]]))


async def pe_rubl(msg, cmd):
    arguments = msg.text.split()
    if len(arguments) < 2:
        await msg.answer(empty_msg)
        return
    val_dif = arguments[1]
    regex_val = r'^[+-]?\d{1,2}$'
    if not re.match(regex_val, val_dif):
        await msg.answer(wrong_format)
        return
    val_dif = int(val_dif)

    student_id = msg.from_user.id
    db.cur.execute(f'SELECT {cmd} FROM Students WHERE id = ?', (student_id,))
    result = db.cur.fetchone()
    if not result:
        await msg.answer(not_yet_registered)
        return
    old_val = result[0]
    new_val = old_val + val_dif
    if (new_val < 0) or (new_val >= 100):
        match cmd:
            case 'pe':
                await msg.answer(pe_err)
            case 'rubl':
                await msg.answer(rubl_err)
        return
    db.cur.execute(f'UPDATE Students SET {cmd} = ? WHERE id = ?', (new_val, student_id))
    db.con.commit()
    match cmd:
        case 'pe':
            await msg.answer(pe_ok.format(old_val, new_val))
        case 'rubl':
            await msg.answer(rubl_ok.format(old_val, new_val))

@db_router.message(Command(commands=['pe', 'физра']))
async def command_pe(msg: Message):
    await pe_rubl(msg, 'pe')

@db_router.message(Command(commands=['rubl', 'рубл', 'рубль']))
async def command_rubl(msg: Message):
    await pe_rubl(msg, 'rubl')
