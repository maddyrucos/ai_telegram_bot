import sqlite3 as sq
import for_admin
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


async def create_profile(user_id, username):

    user = cur.execute(f"SELECT 1 FROM users WHERE user_id == '{user_id}'").fetchone()

    if not user:
        cur.execute(f'INSERT INTO users (user_id, username, approved) VALUES("{user_id}", "{username}", "0")')
        db.commit()


async def check_admin(bot, dp, username, user_id):
    cur.execute(f"SELECT username FROM admins WHERE username == '{username}'")  # берем список админов
    admin = cur.fetchone()
    # если username отсутствует в списке, то ничего не происходит
    if admin == None:
        pass

    else:
        # если username есть в списке, то активируется функция админа
        await for_admin.admin(bot, dp, user_id, db)


def check_approved(username):
    # берем из списка пользователей пункт approved, отвечающий за доступ
    cur.execute(f"SELECT approved FROM users WHERE username == '{username}'")
    approved = cur.fetchone()[0]
    # если username отсутствует в списке, то возвращается 0
    if approved == 0:
        return 0

    # если username есть в списке, то возвращается 1
    else:
        return 1