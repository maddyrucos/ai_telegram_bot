from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
ADMIN = os.getenv('ADMIN')
BOT_NAME = os.getenv('BOT_NAME')