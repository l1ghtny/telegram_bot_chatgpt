from src.modules.logs_setup import logger
from src.modules.open_ai.open_ai_main import multiple_responses

logger = logger.logging.getLogger("bot")


async def msg_process_main(context, message):
    messages_texts = await get_replies(message)
    logger.info('got texts')
    formatted_dialog = await format_dialog(messages_texts, message, context)
    logger.info('formatted into dialog')
    async for value in multiple_responses(formatted_dialog):
        if value:
            yield value
    # reply = await multiple_responses(formatted_dialog)
    # return reply


async def get_replies(message):
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


async def format_dialog(messages_texts, message, context):
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
