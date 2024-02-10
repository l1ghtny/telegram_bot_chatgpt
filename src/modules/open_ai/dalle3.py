import os
import openai
from dotenv import load_dotenv
from openai import OpenAI

from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")

load_dotenv()
openai.organization = "org-dTq0wzkkXgmTQ1GIDabM4fva"
openai.api_key = os.getenv("OPENAI_API_KEY")


async def create_image(prompt):
    client = OpenAI()
    logger.info('Requested an image')
    result = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size='1024x1024'
    )
    logger.info('Image generated')
    image_url = result.data[0].url
    logger.info(image_url)
    logger.info('revised prompt: %s', result.data[0].revised_prompt)
    return image_url
