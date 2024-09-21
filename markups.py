from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Database.database import remove_user

# -- Главное меню --
to_main_menu = InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')
to_menu_only = InlineKeyboardMarkup(inline_keyboard=[[to_main_menu]])

image_button = InlineKeyboardButton(text='Изображение', callback_data='image')
back_to_text = InlineKeyboardButton(text='Назад', callback_data='main_menu')

def create_main_menu(is_approved):
    builder = InlineKeyboardBuilder()
    if is_approved:
        builder.row(image_button)
    else:
        builder.row(InlineKeyboardButton(text='Запросить доступ', url='t.me/madeezy'))
    return builder.as_markup()

# -- Администратор --

admin_add_user = InlineKeyboardButton(text='Добавить пользователя', callback_data='add_user')
admin_remove_user = InlineKeyboardButton(text='Удалить пользователя', callback_data='remove_user')
admin_mailing = InlineKeyboardButton(text='Рассылка', callback_data='mailing')
admin_getdb = InlineKeyboardButton(text='Скачать БД', callback_data='get_db')
admin_menu = InlineKeyboardMarkup(inline_keyboard=[[admin_mailing], [admin_add_user], [admin_remove_user], [admin_getdb]])