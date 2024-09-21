from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

import Database.database as db
import markups as mks
import states

from config import bot

from openpyxl import Workbook

admin = Router()


'''
Рассылка сообщения всем пользователям из БД
Доступно только админу после проверки
'''
# Запрос сообщения. Состояние меняется на принимающее сообщение
@admin.callback_query(F.data=='mailing', states.Admin.default)
async def mailing(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите текст рассылки:')
    await state.set_state(states.Admin.mailing)


# Текст сообщения обработался и отправляется пользователям. Для каждого пользователя происходит try
@admin.message(states.Admin.mailing)
async def get_text(message: types.Message, state: FSMContext):
    users = await db.get_users()
    for user in users:
        try:
            await bot.send_message(chat_id=user[0], text=message.text)
        except Exception as e:
            print(user[0], e.args)

    await state.set_state(states.Admin.default) #возвращаем обычное состояние админа, чтобы сообщения не дублировались всем пользователям
    await bot.send_message(message.from_user.id, 'Сообщение отправлено всем пользователям', reply_markup=mks.to_menu_only)


# Получение списка с пользователями в формате xlsx
@admin.callback_query(F.data=='get_db', states.Admin.default)
async def get_db(callback_query: types.CallbackQuery):
    users = await db.get_users()
    wb = Workbook()
    ws = wb.active
    for user in users:
        ws.append(user)
    wb.save('users.xlsx')
    database = types.FSInputFile('users.xlsx')
    await bot.send_document(callback_query.from_user.id, database)


# Получение id пользователя для разрешения использования ai
@admin.callback_query(F.data=='add_user', states.Admin.default)
async def get_user_id(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите id')
    # Передается состояние добавления пользователя
    await state.set_state(states.Admin.adding_user)


# Получение id пользователя для запрета использования ai
@admin.callback_query(F.data=='remove_user', states.Admin.default)
async def get_user_id(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите id')
    # Передается состояние добавления пользователя
    await state.set_state(states.Admin.removing_user)


# Добавление разрешения пользователю в БД через id
@admin.message(states.Admin.adding_user)
async def add_user(message: types.Message, state: FSMContext):
    await db.add_user(message.text)
    await message.answer('Пользователь добавлен!')
    await state.set_state(states.Admin.default)


# Удаление разрешения пользователю в БД через id
@admin.message(states.Admin.removing_user)
async def remove_user(message: types.Message, state: FSMContext):
    await db.remove_user(message.text)
    await message.answer('Пользователь удален!')
    await state.set_state(states.Admin.default)