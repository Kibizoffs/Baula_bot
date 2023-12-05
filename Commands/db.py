import aiogram
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType
import re

from config import db
from main import bot

db_router = aiogram.Router()

@db_router.message(Command(commands=['passport', 'me', 'паспорт', 'я']))
async def command_passport(msg: Message):
    if msg.chat.type != ChatType.PRIVATE:
        await msg.answer('Вы можете воспользоваться /start только в ЛС')
        return
    student_id = msg.from_user.id
    select_columns = [
        'id', 'last_name', 'first_name',
        'middle_name', 'group_id', 'send_baula_res', 'msg_count_1w']
    db.cur.execute(f"SELECT {', '.join(x for x in select_columns)} FROM Students WHERE ID = ?", (student_id,))
    row = db.cur.fetchone()
    if not row:
        msg.answer('Сперва /register')
        return
    print(row)
    answer = '\n'.join(f'{str(select_columns[i])}: {str(row[i])}' for i in range(len(select_columns)))
    await msg.answer(answer)

@db_router.message(Command(commands=['edit', 'изменить']))
async def command_edit(msg: Message):
    if msg.chat.type != ChatType.PRIVATE:
        await msg.answer('Вы можете воспользоваться /register только в ЛС')
        return
    student_id = msg.from_user.id
    select_columns = ['last_name', 'first_name', 'middle_name', 'group_id', 'send_baula_res', 'msg_count_1w']
    db.cur.execute(f"SELECT {', '.join(x for x in select_columns)} FROM Students WHERE ID = ?", (student_id,))
    result = db.cur.fetchone()
    if not result:
        await msg.answer('Вы ещё не были зарегистрированы')
        return

    arguments = msg.text.split()
    if len(arguments) < 2:
        await msg.answer(
            '/edit <ключ> <значение> - установить значение к ключу в записе о вас в базе данных\n' + \
            "    'last_name' <фамилия>\n" + \
            "    'first_name' <имя>\n" + \
            "    'middle_name' <отчество>\n" + \
            "    'group_id' <группа>\n" + \
            "    'send_baula_res' <0 (отключено) или 1 (включено)> - присылать результаты ср\n" + \
            "    'stats' <-1 (отключено) или 0 (включено)> - участвовать в статистике"
        )
        return
    key = arguments[1].lower()
    val = arguments[2]
    if len(val) > 16:
        await msg.answer('Слишком длинное значение')
        return
    found = False
    for x in select_columns:
        if x == key:
            found = True
            if val == '':
                dr.cur.execute(f'DELETE FROM Students WHERE ID = ? AND {key} = ?')
                await msg.answer(f"Удалил запись")
            else:
                regex_group = re.compile(r'^\d{3}$')
                regex_send_baula_res = re.compile(r'^[01]$')
                regex_msg_count = re.compile(r'^-1|0$')
                if key == 'group_id' and (not regex_group.match(val)) or \
                    key == 'send_baula_res' and (not regex_send_baula_res.match(val)) or \
                    key == 'msg_count_1w' and (not regex_msg_count.match(val)):
                    await msg.answer('Неправильный формат значения')
                    return
                db.cur.execute(f'UPDATE Students SET {key} = ? WHERE ID = ?', (val, student_id))
                db.con.commit()
                await msg.answer(f'Обновили запись')
            break
    if not found:
        await msg.answer('Ключ не был найден')
        return


@db_router.message(Command(commands=['register', 'create', 'создать']))
async def command_register(msg: Message):
    if msg.chat.type != ChatType.PRIVATE:
        await msg.answer('Вы можете воспользоваться /register только в ЛС')
        return
    student_id = msg.from_user.id
    db.cur.execute("SELECT * FROM Students WHERE ID = ?", (student_id,))
    result = db.cur.fetchone()
    if result:
        await msg.answer('Вы уже зарегистрированы')
        return
    db.cur.execute("INSERT INTO Students (ID, send_baula_res, msg_count_1w) VALUES (?, ?, ?)",
        (student_id, 1, 0))
    db.con.commit()
    await msg.answer('Регистрация прошла успешно')
    await msg.answer(
       '/edit <ключ> <значение> - установить значение к ключу в записе о вас в базе данных\n' + \
        "    'last_name' <фамилия>\n" + \
        "    'first_name' <имя>\n" + \
        "    'middle_name' <отчество>\n" + \
        "    'group_id' <группа>\n" + \
        "    'send_baula_res' <0 (отключено) или 1 (включено)> - присылать результаты ср\n" + \
        "    'stats' <-1 (отключено) или 0 (включено)> - участвовать в статистике"
    )

@db_router.message(Command(commands=['delete', 'remove', 'удалить']))
async def command_delete(msg: Message):
    if msg.chat.type != ChatType.PRIVATE:
        await msg.answer('Вы можете воспользоваться /delete только в ЛС')
        return
    student_id = msg.from_user.id
    db.cur.execute("SELECT * FROM Students WHERE ID = ?", (student_id,))
    result = db.cur.fetchone()
    if not result:
        await msg.answer('Вы ещё не были зарегистрированы')
        return
    db.cur.execute("DELETE FROM Students WHERE ID = ?", (student_id,))
    db.con.commit()
    await msg.answer('Учётная запись была удалена')
