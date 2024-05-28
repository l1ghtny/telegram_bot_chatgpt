import os

from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("TOKEN")
bot_test_token = os.getenv('bot_test_token')
database_url_local = os.getenv("database_url_local")
