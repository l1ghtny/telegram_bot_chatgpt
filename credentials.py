import os

from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("TOKEN")
bot_test_token = os.getenv('bot_test_token')
database_url_local = os.getenv("database_url_local")
openai_api_key = os.getenv("OPENAI_API_KEY")
terminal_key = os.getenv("TERMINAL_KEY")
terminal_pass = os.getenv("TERMINAL_PASS")
serpapi_key = os.getenv("SERP_API_KEY")
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
terminal_key = os.getenv("TERMINAL_KEY")
terminal_pass = os.getenv("TERMINAL_PASS")
serpapi_key = os.getenv("SERP_API_KEY")
