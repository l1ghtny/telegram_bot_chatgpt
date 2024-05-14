from typing import AsyncIterable

from src.modules.logs_setup import logger
from src.modules.open_ai.open_ai_main import get_gpt4_response

logger = logger.logging.getLogger("bot")


async def msg_process_main(context, message, multiple: bool) -> AsyncIterable:
    if multiple:
        messages_texts = await get_replies(message)
        logger.info('got texts')
        formatted_dialog = await format_dialog(messages_texts, message, context)
        logger.info('formatted into dialog')
        async for value in get_gpt4_response(formatted_dialog):
            if value:
                yield value
    else:
        logger.info('Getting message text')
        message_meaning = message.text.replace(f'@{context.bot.username} ', '')
        messages = [{"role": "user", "content": f"{message_meaning}"}]
        async for value in get_gpt4_response(messages):
            if value:
                value_edited = value.replace('#', '')
                # value_edited = value_edited1.replace('**', '*')
                yield value_edited


async def get_replies(message) -> list:
    messages_text = []
    while message.reply_to_message is not None:
        message = message.reply_to_message
        text = message.text
        author_id = message.from_user.id
        messages_text.append({
            'author': author_id,
            'text': text
        })
    return messages_text


async def format_dialog(messages_texts, message, context) -> list:
    messages_texts.reverse()
    dialog_formatted = []
    for i in messages_texts:
        if f'@{context.bot.username}' in i['text']:
            content = i['text']
            new_message = content.replace(f'<@{content.bot.username}>', '')
            dialog_formatted.append({'role': 'user', 'content': new_message})
        elif i['author'] == context.bot.id:
            message_text = i['text']
            dialog_formatted.append({'role': 'assistant', 'content': message_text})
        else:
            message_text = i['text']
            dialog_formatted.append({'role': 'user', 'content': message_text})
    # adding the last message
    dialog_formatted.append({'role': 'user', 'content': message.text})
    return dialog_formatted
