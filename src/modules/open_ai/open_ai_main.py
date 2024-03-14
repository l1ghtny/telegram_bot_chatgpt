import logging
import os
import openai
from dotenv import load_dotenv
from openai import OpenAI

from src.modules.logs_setup import logger

load_dotenv()
openai_organization = "org-dTq0wzkkXgmTQ1GIDabM4fva"
openai_api_key = os.getenv("OPENAI_API_KEY")
model3 = 'gpt-3.5-turbo-16k'
model4 = 'gpt-4-turbo-preview'
role = """You are a nice and articulated helper"""

logger = logger.logging.getLogger('bot')


async def get_gpt4_response(messages):
    try:
        all_messages = [{"role": "system", "content": f"{role}"}] + messages
        logger.info('Accessing OpenAI API')
        client_ai = OpenAI(api_key=openai_api_key, organization=openai_organization)
        response = client_ai.chat.completions.create(
            model=model4,
            messages=all_messages,
            stream=True
        )
        logger.info('success')
    except Exception as e:
        logger.exception(e)
    completion_text = ''
    try:
        for event in response:
            if event.choices[0].delta.content is not None:
                event_text = event.choices[0].delta.content
                completion_text += event_text
                yield completion_text
    except Exception as e:
        logger.exception(e)
        completion_text = 'There was an error on the side of the API'
    yield completion_text
