from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# -- Главное меню --

start_text_button = InlineKeyboardButton('Текст', callback_data='text')
start_image_button = InlineKeyboardButton('Изображение', callback_data='image')
start_menu = InlineKeyboardMarkup(row_width=1).add(start_text_button, start_image_button)

# -- Администратор --

admin_add_user = InlineKeyboardButton('Добавить пользователя', callback_data='add_user')
admin_send = InlineKeyboardButton('Отправить сообщение', callback_data='send_button')
admin_download = InlineKeyboardButton('Выгрузить базу', callback_data='download')
admin_menu = InlineKeyboardMarkup(row_width=1).add(admin_add_user, admin_send, admin_download)