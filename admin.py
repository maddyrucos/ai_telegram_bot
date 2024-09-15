from aiogram import types, Router, F
from aiogram.utils import exceptions
from aiogram.filters.command import Command

import states
from openpyxl import Workbook
import asyncio

import markups as mks

admin = Router()


#Рассылка сообщения всем пользователям
@admin.callback_query(F.data='mailing', states.Admin.default)
async def start(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Введите текст рассылки:')


@admin.message(content_types=['text'], state = Admin.sending_message) #принимаем сообщение, действует только при состоянии Admin.sending_message
async def get_text(message: types.Message):
    text = message.text #присваиваем текст сообщения от пользователя (администратора) в переменную, которую передадим как текст сообщения бота
    cur.execute('SELECT user_id FROM users') #выделяем всех пользователей из базы данных
    user = cur.fetchall() #помещаем всех пользователей из бд в переменную
    for row in user: #для каждого ряда из списка пользователей
        #создаем исключение с рядом возможных ошибок
        try:
            await bot.send_message(row[0], text)
        except exceptions.BotBlocked:
            print(f"Пользователь {user} заблокировал этого бота")
        except exceptions.ChatNotFound:
            print(f"Чат пользователя {user} не найден")
        except exceptions.RetryAfter as e:
            print(f"Апи отправило слишком много запросов, нужно немного подождать {e.timeout} секунд")
            await asyncio.sleep(e.timeout)
        except exceptions.TelegramAPIError:
            print(f"Ошибка Telegram API для пользователя {user}")

    await Admin.default.set() #возвращаем обычное состояние админа, чтобы сообщения не дублировались всем пользователям
    await bot.send_message(message.from_user.id, 'Сообщение отправлено всем пользователям', reply_markup=mks.to_menu_markup)


#выгрузка базы данных
@admin.callback_query(lambda c: c.data and 'download' in c.data, state = Admin.default)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    cur.execute('SELECT * FROM users')  # выбираем всю таблицу users
    data = cur.fetchall()  # передаем
    wb = Workbook()  # создаем воркбук для конвертирования бд
    ws = wb.active
    for row in data:
        ws.append(row)
    wb.save('users.xlsx')
    with open('users.xlsx', "rb") as file:
        await bot.send_document(callback_query.from_user.id, file, reply_markup=mks.admin_menu)


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
    await message.answer('Пользователь добавлен', reply_markup=mks.admin_menu)