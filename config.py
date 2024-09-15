from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN') # admin username

# API-KEYS FOR AI
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
MISTAL_TOKEN = os.getenv('MISTRAL_TOKEN')