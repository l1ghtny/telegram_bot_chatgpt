import os
import openai
from dotenv import load_dotenv
from openai import OpenAI

from modules.logs_setup import logger

load_dotenv()
openai.organization = "org-dTq0wzkkXgmTQ1GIDabM4fva"
openai.api_key = os.getenv("OPENAI_API_KEY")
# model = 'gpt-3.5-turbo-16k'
model = 'gpt-4-1106-preview'
role = """Ты - помощник по всем айти вопросам"""

logger = logger.logging.getLogger("bot")


async def one_response(message):
    client_ai = OpenAI()
    response = client_ai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"{role}"},
            {"role": "user", "content": f"{message}"}
        ]
    )
    logger.info('success')
    reply = response.choices[0].message.content
    content = reply
    # tokens_total = response.usage.total_tokens
    return content


async def multiple_responses(messages):
    client_ai = OpenAI()
    response = client_ai.chat.completions.create(
        model=model,
        messages=messages
    )
    logger.info('success')
    reply = response.choices[0].message.content
    return reply
