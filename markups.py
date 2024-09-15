from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
'''
# -- Администратор --

admin_add_user = InlineKeyboardButton('Добавить пользователя', callback_data='add_user')
admin_send = InlineKeyboardButton('Отправить сообщение', callback_data='send_button')
admin_download = InlineKeyboardButton('Выгрузить базу', callback_data='download')
admin_menu = InlineKeyboardMarkup(row_width=1).add(admin_add_user, admin_send, admin_download)'''