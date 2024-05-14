import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from src.modules.logs_setup import logger

load_dotenv()
openai_organization = "org-dTq0wzkkXgmTQ1GIDabM4fva"
openai_api_key = os.getenv("OPENAI_API_KEY")
model3 = 'gpt-3.5-turbo-16k'
model4 = 'gpt-4-turbo-preview'
model4o = 'gpt-4o'
role = """You are a nice and articulated helper"""

logger = logger.logging.getLogger('bot')
client_ai = AsyncOpenAI(api_key=openai_api_key, organization=openai_organization)


async def get_gpt4_response(messages):
    try:
        all_messages = [{"role": "system", "content": f"{role}"}] + messages
        logger.info('Accessing OpenAI API')
        response = await client_ai.chat.completions.create(
            model=model4,
            messages=all_messages,
            stream=True,
            stream_options={"include_usage": True}
        )
        logger.info('success')
    except Exception as e:
        logger.exception(e)
    completion_text = ''
    try:
        async for event in response:
            if event.choices and event.choices[0].delta.content:
                event_text = event.choices[0].delta.content
                completion_text += event_text
                yield completion_text
            if event.usage is not None:
                # record usage
                pass
    except Exception as e:
        logger.exception(e)
        completion_text = 'There was an error on the side of the API'
        yield completion_text
