import sqlite3 as sq
import os

import config

os.chdir('Database')
db = sq.connect('gpt.db')
cur = db.cursor()
os.chdir('..')

async def init_db():

    #Таблица пользователей
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id          INTEGER PRIMARY KEY,
    username         TEXT,
    approved         INTEGER
    )''')
    db.commit()

    #Таблица администраторов
    cur.execute("CREATE TABLE IF NOT EXISTS admins(username TEXT PRIMARY KEY)")

    try:
        cur.execute(f'INSERT INTO admins(username) VALUES("{config.ADMIN}")')
    except:
        pass

    db.commit()


'''
Создание профиля в БД + проверка на доступ к функциям ИИ.
Подробнее расписано в main.py в комментарии к /start
'''
async def create_profile(user_id, username):
    user = cur.execute(f"SELECT * FROM users WHERE user_id == '{user_id}'").fetchone()
    if not user:
        cur.execute(f'INSERT INTO users (user_id, username, approved) VALUES("{user_id}", "{username}", "0")')
        db.commit()
        return 0
    else:
        return user[2]


# Проверка на админа в БД по username
async def check_admin(username):
    if cur.execute(f"SELECT 1 FROM admins WHERE username == '{username}'").fetchone():
        return 1
    else:
        return 0


# Добавление пользователю возможности пользоваться нейросетью
async def add_user(id):
    try:
        cur.execute(f'UPDATE users SET "approved"="1" WHERE "user_id"=="{id}"')
        db.commit()
        return 1
    except:
        return 0


async def remove_user(id):
    try:
        cur.execute(f'UPDATE users SET "approved"="0" WHERE "user_id"=="{id}"')
        db.commit()
        return 1
    except:
        return 0


# Получение полного списка пользователей
async def get_users():
    return cur.execute('SELECT * FROM users').fetchall()
