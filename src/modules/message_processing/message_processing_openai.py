from typing import AsyncIterable

import telegram

from src.modules.chat_bot.open_ai.open_ai_main import get_gpt4_response
from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


async def msg_process_main(context, message, multiple: bool, effective_user: telegram._update.Update.effective_user) -> AsyncIterable:
    logger.info('process main')
    try:
        # user_exists = await check_user_exists(effective_user.id)
        # if not user_exists:
        #     await add_user(effective_user.id, payment_plan_id=1, country_id=1, tg_tag=effective_user.username)
        # user = await get_user_by_tg_id(effective_user.id)
        if multiple:
            messages_texts = await get_replies(message)
            logger.info('got texts')
            formatted_dialog = await format_dialog(messages_texts, message, context)
            logger.info('formatted into dialog')
            async for value in get_text_from_gpt(formatted_dialog, user):
                if value:
                    yield value
        else:
            logger.info('Getting message text')
            message_meaning = message.text.replace(f'@{context.bot.username} ', '')
            messages = [{"role": "user", "content": f"{message_meaning}"}]
            async for value in get_text_from_gpt(messages, user):
                yield value
    except Exception as e:
        logger.exception(e)


async def get_text_from_gpt(messages, user):
    async for value, usage in get_gpt4_response(messages):
        if value:
            value_edited = value.replace('#', '')
            value_edited = value_edited.replace('!', '\\!')
            value_edited = value_edited.replace('.', '\\.')
            value_edited = value_edited.replace('?', '\\?')
            value_edited = value_edited.replace(',', '\\,')
            value_edited = value_edited.replace(';', '\\;')
            value_edited = value_edited.replace('=', '\\=')
            value_edited = value_edited.replace('-', '\\-')
            value_edited = value_edited.replace(')', '\\)')
            value_edited = value_edited.replace('(', '\\(')
            value_edited = value_edited.replace('**', '*')
            value_edited = value_edited.replace('+', '\\+')
            yield value_edited
        # if usage:
        #     try:
        #         await add_gpt_usage(user, usage.prompt_tokens, usage.completion_tokens)
        #     except Exception as e:
        #         logger.error(e)


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
