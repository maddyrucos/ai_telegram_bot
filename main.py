from aiogram import Router, types, F, Dispatcher
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from admin import admin

import states

from Database import database as db
import markups as mks
from config import bot
import config

#from AI import gpt
from AI import mistral
import asyncio


router = Router()
dp = Dispatcher()
dp.include_router(router)
dp.include_router(admin)


# Инициализация БД при запуске бота
async def on_startup(_):
    await db.init_db()


@router.message(Command('start'))
async def command_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    await state.set_state(states.Approvement.not_approved)

    '''
    Проверка на доступ к возможностям бота.
    Функция create_profile возвращает 0, если пользователя не было в БД, иначе вернет его approved
    Допуск есть, если approved = 0
    '''
    if await db.create_profile(user_id, username):
        welcomeText = (f'Приветствую! Вы можете познать все прелести современной нейросети!\n'
                       f'Просто напишите свой вопрос в чат, либо нажмите кнопку, чтобы создать изображение')
        await state.set_state(states.Approvement.approved)
        await bot.send_message(message.from_user.id, welcomeText, reply_markup=mks.create_main_menu(True))
    else:
        welcomeText = (f'Приветствую! К сожалению, у Вас нет доступа.\nОбратитесь к @{config.ADMIN}')
        await bot.send_message(message.from_user.id, welcomeText, reply_markup=mks.create_main_menu(False))



@router.message(Command('admin'))
async def command_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    # Проверка на наличие прав администратора
    if await db.check_admin(user_id, username):
        #admin.admin(bot, router, user_id, db)
        await state.set_state(states.Admin.default)
        await message.answer('Админ меню', reply_markup=mks.admin_menu)
    else:
        await message.answer('У вас нет доступа!')


@router.message(states.Approvement.approved)
async def get_text(message: types.Message, state: FSMContext):
    response_message = await bot.send_message(message.from_user.id, 'Ожидание ответа...')
    ai_response = await mistral.get_response(message.text)
    await response_message.edit_text(ai_response)


@router.callback_query(F.data == 'image', states.Approvement.approved)
async def main_menu(callback_query: types.callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer('Напишите описание желаемой картинки.')
    await state.set_state(states.Approvement.image)


async def main():
    await db.init_db()
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())