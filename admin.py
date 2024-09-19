from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from openpyxl import Workbook
import asyncio

import Database.database as db
import markups as mks
import states

from config import bot

admin = Router()


'''
Рассылка сообщения всем пользователям из БД
Доступно только админу после проверки
'''
# Запрос сообщения. Состояние меняется на принимающее сообщение
@admin.callback_query(F.data=='mailing', states.Admin.default)
async def start(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите текст рассылки:')
    await state.set_state(states.Admin.mailing)


# Текст сообщения обработался и отправляется пользователям. Для каждого пользователя происходит try
@admin.message(states.Admin.mailing)
async def get_text(message: types.Message, state: FSMContext):
    users = await db.get_users()
    for user in users:
        try:
            print(user)
            await bot.send_message(chat_id=user[0], text=message.text)
        except Exception as e:
            print(user[0], e.args)

    await state.set_state(states.Admin.default) #возвращаем обычное состояние админа, чтобы сообщения не дублировались всем пользователям
    await bot.send_message(message.from_user.id, 'Сообщение отправлено всем пользователям', reply_markup=mks.to_menu_only)


# Получение списка с пользователями в формате xlsx
@admin.callback_query(F.data=='get_db', states.Admin.default)
async def process_callback_button1(callback_query: types.CallbackQuery):
    users = await db.get_users()
    wb = Workbook()
    ws = wb.active
    for user in users:
        ws.append(user)
    wb.save('users.xlsx')
    database = types.FSInputFile('users.xlsx')
    await bot.send_document(callback_query.from_user.id, database)

'''
#возврат в меню админа
@admin.callback_query(lambda c: c.data and 'admin' in c.data, state = Admin.default)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(user_id, 'Меню администратора', reply_markup=mks.admin_menu)


@admin.callback_query(lambda c: c.data and 'add_user' in c.data, state=Admin.default)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(user_id, 'Введите имя пользователя')
    # Передается состояние добавления пользователя
    await Admin.adding_user.set()


# принимаем сообщение, действует только при состоянии Admin.sending_message
@admin.message(content_types=['text'], state=Admin.adding_user)
async def get_username(message: types.Message):
    # Получение текста сообщения с никнеймом
    text = message.text
    # Изменение пункта approved (отвечает за доступ) на 1 (допуск) там, где username = полученному выше
    cur.execute(f'UPDATE users SET approved = "1" WHERE username == "{text}"')
    db.commit()
    await message.answer('Пользователь добавлен', reply_markup=mks.admin_menu)'''