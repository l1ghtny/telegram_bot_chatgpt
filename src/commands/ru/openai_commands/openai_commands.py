import datetime
import re

import telegram
from telegram import Update, BotCommandScopeChat
from telegram.ext import ContextTypes, ConversationHandler

from src.commands.ru.desc import commands
from src.modules.chat_bot.misc.actions import send_upload_photo_action
from src.modules.chat_bot.open_ai.dalle3 import create_image
from src.modules.logs_setup import logger
from src.modules.message_processing.message_processing_openai import msg_process_main

logger = logger.logging.getLogger("bot")

RESPONSE = 0
ASKED = 1


async def check_for_gpt_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    message_text = message.text
    if f'@{context.bot.username}' in message_text:
        logger.info('Replying to message %s', message.text)
        first_reply = await update.effective_message.reply_text(text='Thinking...', reply_to_message_id=message.id)
        current_time = datetime.datetime.now()
        async for value in msg_process_main(context, message, False, effective_user=update.effective_user):
            if re.search('[A-Za-zА-яЁё]', value):
                timedelta = datetime.datetime.now() - current_time
                if timedelta.seconds > 3 and first_reply.text:
                    await first_reply.edit_text(value)
                    current_time = datetime.datetime.now()
        logger.info('Finished fetching reply')
        if first_reply.text != value:
            await first_reply.edit_text(value)
        logger.info('All done')

    elif message.reply_to_message is not None:
        reply_user = message.reply_to_message.from_user
        if reply_user.id == context.bot.id and message.reply_to_message.text:
            logger.info('Replying to message %s', message.text)
            first_reply = await update.effective_message.reply_text(text='Думаю...', reply_to_message_id=message.id)
            current_time = datetime.datetime.now()
            async for value in msg_process_main(context, message, True, effective_user=update.effective_user):
                if re.search('[A-Za-zА-яЁё]', value):
                    timedelta = datetime.datetime.now() - current_time
                    if timedelta.seconds > 3 and first_reply.text:
                        try:
                            await first_reply.edit_text(value, parse_mode='MarkdownV2')
                        except Exception as e:
                            logger.error(e)
                        current_time = datetime.datetime.now()
            logger.info('Finished fetching reply')
            if first_reply.text != value:
                await first_reply.edit_text(value, parse_mode='MarkdownV2')
        logger.info('All done')


async def start2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        logger.info('GPT4 Command used')
        await update.message.reply_text('Напиши вопрос \n'
                                        'Если хочешь отменить диалог, используй /cancel_chat \nЧтобы продолжить диалог, ответьте на предыдущее сообщение бота')
    except telegram.error as e:
        logger.exception(e)

    return ASKED


async def response2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        message = await update.effective_message.reply_text('Думаю...', reply_to_message_id=update.message.message_id)
        current_time = datetime.datetime.now()
        async for value in msg_process_main(context, update.effective_message, False, effective_user=update.effective_user):
            if re.search('[A-Za-zА-яЁё]', value):
                timedelta = datetime.datetime.now() - current_time
                if timedelta.seconds > 3 and message.text:
                    await message.edit_text(text=value, parse_mode='MarkdownV2')
                    current_time = datetime.datetime.now()
        logger.info('Finished fetching reply')
        if message.text != value:
            await message.edit_text(text=value, parse_mode='MarkdownV2')
        logger.info('All done')
    except telegram.error as e:
        logger.exception(e)
        await update.effective_message.reply_text('Произошла какая-то ошибка, обратитесь к админу бота')

    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info('Dalle3 Started')
    await update.message.reply_text('Напиши текст, по которому сгенерировать изображение: \n'
                                    'Используй /cancel_generation чтобы отменить запрос. ')

    return RESPONSE


@send_upload_photo_action
async def response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = await update.effective_message.reply_text('Генерирую изображение... Это может занять некоторое время...')
    image_url = await create_image(update.effective_message.text)
    await message.delete()
    await update.effective_chat.send_photo(image_url)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info('cancelled')
    await update.effective_message.reply_text('Запрос отменён')

    return ConversationHandler.END


async def secret_access(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info('Secret access requested by user %s', update.effective_user.username)
    await context.bot.set_my_commands(commands=commands, scope=BotCommandScopeChat(chat_id=update.effective_chat.id))
    await update.message.reply_text('Команды добавлены')


async def secret_access_remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info('User %s removed secret access', update.effective_user.username)
    await context.bot.set_my_commands(commands=[], scope=BotCommandScopeChat(chat_id=update.effective_chat.id))
    await update.message.reply_text('Доступ убран')
