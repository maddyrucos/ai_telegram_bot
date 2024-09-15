from aiogram import Router, Bot, types, F, Dispatcher
from aiogram.filters.command import Command, CommandObject

#import admin

from Database import database as db
#import markups as mks
import config

#import gpt
import asyncio


bot = Bot(token=config.BOT_TOKEN)
router = Router()
dp = Dispatcher()
dp.include_router(router)


# Инициализация БД при запуске бота
async def on_startup(_):
    await db.init_db()



@router.message(Command('start'))
async def command_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    '''
    Проверка на доступ к возможностям бота.
    Функция create_profile возвращает 0, если пользователя не было в БД, иначе вернет его approved
    Допуск есть, если approved = 0
    '''
    if await db.create_profile(user_id, username):
        welcomeText = (f'Приветствую! Вы можете познать все прелести современной нейросети!')
        await bot.send_message(message.from_user.id, welcomeText)
    else:
        welcomeText = (f'Приветствую! К сожалению, у Вас нет доступа.\nОбратитесь к @{config.ADMIN}')
        await bot.send_message(message.from_user.id, welcomeText)


# Хендлер, который срабатывает при вводе пользователем "/admin"
@router.message(Command('admin'))
async def command_start(message: types.Message ):
    user_id = message.from_user.id
    username = message.from_user.username
    # Проверка на наличие прав администратора
    if await db.check_admin(user_id, username):
        admin.admin(bot, router, user_id, db)


@router.callback_query(F.data == 'text')
async def main_menu(callback_query: types.callback_query):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.answer('Введите свой вопрос.')

    await Approved.text.set()


@router.callback_query(F.data == 'image')
async def main_menu(callback_query: types.callback_query):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.answer('Напишите описание желаемой картинки.')

    await Approved.image.set()


@router.message()
async def get_text(message: types.Message):

    response_message = await bot.send_message(message.from_user.id, 'Ожидание ответа...')

    chat_gpt_response = gpt.generate_response(message.text)

    await response_message.edit_text(chat_gpt_response)

    await bot.send_message(message.from_user.id, 'Продолжим?', reply_markup=mks.start_menu)


@router.message()
async def get_text(message: types.Message):

    response_message = await bot.send_message(message.from_user.id, 'Ожидание ответа...')

    chat_gpt_response = gpt.generate_image(message.text, message.from_user.username)

    await response_message.delete()

    if chat_gpt_response != None:

        await bot.send_photo(message.from_user.id, types.InputFile(f'{message.from_user.username}.png'))

    else:

        await bot.send_message(message.from_user.id, 'Возникла ошибка!')

    await bot.send_message(message.from_user.id, 'Продолжим?', reply_markup=mks.start_menu)



async def main():
    await db.init_db()
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())