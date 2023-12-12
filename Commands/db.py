import aiogram
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import re

from Events.messages import parse_msg
from config import db
from main import bot
from vars import *

db_router = aiogram.Router()

@db_router.message(Command(commands=['chat', 'чат']))
async def command_chat(msg: Message):
    await parse_msg(msg)

    chat = msg.chat
    db.cur.execute("SELECT gr FROM Groups WHERE id = ?", (chat.id,))
    res = db.cur.fetchone()
    gr = chat_passport_gr.format(NIL)
    if res:
        if res[0]:
            gr = chat_passport_gr.format(str(res[0]))

    await msg.answer(
        text=
            id_.format(chat.id) +
            gr,
        parse_mode='HTML'
    )

@db_router.message(Command(commands=['passport', 'me', 'паспорт', 'я']))
async def command_passport(msg: Message):
    await parse_msg(msg)

    user_id = msg.from_user.id
    select_columns = [
        id_key, gr_key, last_name_key,
        pe_key, rubl_key, msg_count_1w_key
    ]
    db.cur.execute(f"SELECT {', '.join(x for x in select_columns)} FROM Students WHERE id = ?", (user_id,))
    res = db.cur.fetchone()
    gr = ''
    last_name = ''
    pe = ''
    rubl = ''
    msg_count_1w = ''
    if res:
        if res[1] != None: gr = chat_passport_gr.format(res[1])
        if res[2] != None: last_name = passport_last_name.format(res[2])
        if res[3] != None: pe = passport_pe.format(res[3])
        if res[4] != None: rubl = passport_rubl.format(res[4])
        if res[5] != None: msg_count_1w = passport_msg_count_1w.format(res[5])

    await msg.answer(
        text=
            id_.format(user_id) + 
            gr +
            last_name.format(last_name) +
            pe.format(pe) +
            rubl.format(rubl) +
            msg_count_1w.format(msg_count_1w),
        parse_mode='HTML'
    )

@db_router.message(Command(commands=['edit', 'изменить']))
async def command_edit(msg: Message):
    await parse_msg(msg)

    arguments = msg.text.split()
    if len(arguments) < 2:
        await msg.answer(
            text=edit_txt.format(gr_key, last_name_key, gr_key, last_name_key),
            parse_mode='HTML'
        )
        return
    key = arguments[1].lower()
    val = arguments[2]
    if len(val) > 16:
        await msg.answer(too_long_message)
        return
        
    user_id = msg.from_user.id
    select_columns = [
        gr_key, last_name_key
    ]
    db.cur.execute(f"SELECT {', '.join(x for x in select_columns)} FROM Students WHERE id = ?", (user_id,))
    result = db.cur.fetchone()
    if not result:
        await msg.answer(not_yet_registered)
        return

    found = False
    for column in select_columns:
        if column == key:
            found = True

            if val == '':
                val = None
            else:
                if key == 'gr':
                    regex_gr = r'^\d{3}$'
                    if not re.match(regex_gr, val):
                        await msg.answer(edit_wrong_gr_format)
                        return

                    val = int(val)
                    db.cur.execute(f"SELECT * FROM Groups WHERE gr = ?", (val,))
                    result = db.cur.fetchone()
                    if not result:
                        await msg.answer(edit_group_doesnt_exist)
                        return
                    elif val in rubl_prac_groups:
                        db.cur.execute(f'UPDATE Students SET pe = 0, rubl = 0, msg_count_1w = 0 WHERE id = ?', (user_id,))

                elif key == 'last_name':
                    regex_last_name = r'^[А-я,-]+$'
                    if not re.match(regex_last_name, val):
                        await msg.answer(edit_wrong_last_name_format)
                        return
                    val = val.title()

            db.cur.execute(f'UPDATE Students SET {key} = ? WHERE id = ?', (val, user_id))
            db.con.commit()
            await msg.answer(edit_updated)
            break

    if not found:
        await msg.answer(edit_key_not_found)
        return

@db_router.message(Command(commands=['register', 'create', 'зарегистрироваться', 'создать']))
async def command_register(msg: Message):
    await parse_msg(msg)

    user_id = msg.from_user.id
    db.cur.execute("SELECT * FROM Students WHERE id = ?", (user_id,))
    result = db.cur.fetchone()
    if result:
        await msg.answer(already_registered)
        return

    db.cur.execute("INSERT INTO Students (id) VALUES (?)", (user_id,))
    db.con.commit()
    await msg.answer(
        text=
            register_ok +
            edit_txt.format(gr_key, last_name_key, gr_key, last_name_key),
        parse_mode='HTML'
    )


@db_router.message(Command(commands=['delete', 'remove', 'удалить']))
async def command_delete(msg: Message):
    await parse_msg(msg)
    
    user_id = msg.from_user.id
    db.cur.execute("SELECT * FROM Students WHERE id = ?", (user_id,))
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
    user_id = query.from_user.id
    if query.data == 'cancel_deletion':
        await query.message.answer(delete_cancelled)
    elif query.data == 'confirm_deletion':
        db.cur.execute("DELETE FROM Students WHERE id = ?", (user_id,))
        db.con.commit()
        await query.message.answer(delete_ok.format(FATAL_ERROR))

    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[[]]))


@db_router.message(Command(commands=['pe', 'физра', 'rubl', 'рубл', 'рубль']))
async def pe_rubl(msg: Message):
    await parse_msg(msg)

    arguments = msg.text.split()
    if len(arguments) < 2:
        await msg.answer(empty_msg)
        return
    cmd = arguments[0]
    val_dif = arguments[1]
    regex_val = r'^[+-]?\d{1,2}$'
    if not re.match(regex_val, val_dif):
        await msg.answer(pe_rubl_bad_nums)
        return
    val_dif = int(val_dif)

    user_id = msg.from_user.id
    db.cur.execute(f'SELECT {gr_key}, {cmd} FROM Students WHERE id = ?', (user_id,))
    res = db.cur.fetchone()
    if not res:
        await msg.answer(not_yet_registered)
        return
    elif cmd == 'rubl' and res[0] not in rubl_prac_groups:
        await msg.answer(not_in_107_108)
        return

    elif res[1] == None:
        old_val = 0
    else:
        old_val = res[1]
    new_val = old_val + val_dif
    if new_val > 100:
        await msg.answer(pe_rubl_overflow)
        return
    elif new_val < 0:
        new_val = 0

    db.cur.execute(f'UPDATE Students SET {cmd} = ? WHERE id = ?', (new_val, user_id))
    db.con.commit()
    match cmd:
        case 'pe':
            await msg.answer(pe_ok.format(old_val, new_val))
        case 'rubl':
            await msg.answer(rubl_ok.format(old_val, new_val))
