from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from states import NotApproved, Approved

from Database import database as db
import markups as mks
import config

import gpt

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Функция инициализирующая БД
async def on_startup(_):
    await db.init_db()

# Хендлер, который срабатывает при вводе пользователем "/start"
@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message):

    # Сбор данных о пользователе
    user_id = message.from_user.id
    username = message.from_user.username

    await NotApproved.default.set()

    # Вызов функции создания профиля (передачи данных в БД)
    await db.create_profile(user_id, username)

    approve_check = db.check_approved(username)

    if approve_check == 1:

        # Приветственное сообщение для пользователя с доступом
        welcomeText = (f'Добро пожаловать в {config.BOT_NAME}! Вы можете познать все прелести '
                       f'современной нейросети!')

        await Approved.default.set()

        await bot.send_message(message.from_user.id, welcomeText,
                               reply_markup=mks.start_menu)

    if approve_check == 0:

        # Приветственное сообщение для пользователя без доступа
        welcomeText = (f'Добро пожаловать в {config.BOT_NAME}! К сожалению, у Вас нет доступа.\n'
                       f'Обратитесь к @{config.ADMIN}')

        await bot.send_message(message.from_user.id, welcomeText)


# Хендлер, который срабатывает при вводе пользователем "/admin"
@dp.message_handler(commands=['admin'], state = '*')
async def admin(message: types.Message):

    # Проверка на наличие прав администратора
    await db.check_admin(bot, dp, message.from_user.username, message.from_user.id)


@dp.callback_query_handler(lambda c: c.data == 'text', state = '*')
async def main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.answer('Введите свой вопрос.')

    await Approved.text.set()


@dp.callback_query_handler(lambda c: c.data == 'image', state='*')
async def main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.answer('Напишите описание желаемой картинки.')

    await Approved.image.set()


@dp.message_handler(state=Approved.text)
async def get_text(message: types.Message):

    response_message = await bot.send_message(message.from_user.id, 'Ожидание ответа...')

    chat_gpt_response = gpt.generate_response(message.text)

    await response_message.edit_text(chat_gpt_response)

    await bot.send_message(message.from_user.id, 'Продолжим?', reply_markup=mks.start_menu)


@dp.message_handler(state=Approved.image)
async def get_text(message: types.Message):

    response_message = await bot.send_message(message.from_user.id, 'Ожидание ответа...')

    chat_gpt_response = gpt.generate_image(message.text, message.from_user.username)

    await response_message.delete()

    if chat_gpt_response != None:

        await bot.send_photo(message.from_user.id, types.InputFile(f'{message.from_user.username}.png'))

    else:

        await bot.send_message(message.from_user.id, 'Возникла ошибка!')

    await bot.send_message(message.from_user.id, 'Продолжим?', reply_markup=mks.start_menu)



if __name__ == '__main__':
    executor.start_polling(dp,
                        skip_updates=True,
                        on_startup=on_startup)