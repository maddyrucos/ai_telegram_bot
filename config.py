from aiogram import Bot
from dotenv import load_dotenv
import logging
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN') # admin username

# API-KEYS FOR AI
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
MISTRAL_TOKEN = os.getenv('MISTRAL_TOKEN')

#logging.basicConfig(filename='bot.logs', filemode='a', level=0)

bot = Bot(token=BOT_TOKEN)