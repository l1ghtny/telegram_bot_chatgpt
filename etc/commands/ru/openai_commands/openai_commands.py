import datetime
import re

from telegram import Update
from telegram.ext import ContextTypes

from etc.modules.message_processing.message_processing import msg_process_main
from etc.modules.open_ai.open_ai_main import one_response
from etc.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")

RESPONSE = 1
ASKED = 1


async def check_for_gpt_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    message_text = message.text
    if f'@{context.bot.username}' in message_text:
        first_reply = await update.effective_message.reply_text(text='Thinking...', reply_to_message_id=message.id)
        message_text_meaning = message_text.replace(f'@{context.bot.username} ', '')
        logger.info(f'asking the question:{message_text_meaning}')
        current_time = datetime.datetime.now()
        async for value in one_response(message_text_meaning):
            if re.search('[A-Za-zА-яЁё]', value):
                timedelta = datetime.datetime.now() - current_time
                if timedelta.seconds > 3 and first_reply.text:
                    await first_reply.edit_text(text=value)
                    current_time = datetime.datetime.now()
        if first_reply.text != value:
            await first_reply.edit_text(text=value)
        logger.info('success')

    elif message.reply_to_message is not None:
        reply_user = message.reply_to_message.from_user
        if reply_user.id == context.bot.id:
            logger.info('Replying to message %s', message.text)
            first_reply = await update.effective_message.reply_text(text='Thinking...', reply_to_message_id=message.id)
            current_time = datetime.datetime.now()
            async for value in msg_process_main(context, message):
                if re.search('[A-Za-zА-яЁё]', value):
                    timedelta = datetime.datetime.now() - current_time
                    if timedelta.seconds > 3 and first_reply.text:
                        await first_reply.edit_text(value)
                        current_time = datetime.datetime.now()
            logger.info('Finished fetching reply')
            if first_reply.text != value:
                await first_reply.edit_text(value)
    logger.info('All done')


async def start2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info('GPT4 Command used')
    await update.message.reply_text('Напиши вопрос \n'
                                    'Если хочешь отменить диалог, используй /cancel_chat')

    return ASKED


async def response2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = await update.effective_message.reply_text('Думаю...')
    message_text_meaning = update.effective_message.text
    current_time = datetime.datetime.now()
    async for value in one_response(message_text_meaning):
        if re.search('[A-Za-zА-яЁё]', value):
            timedelta = datetime.datetime.now() - current_time
            print(timedelta)
            if timedelta.seconds > 3 and message.text:
                await message.edit_text(text=value)
                current_time = datetime.datetime.now()
    if message.text != value:
        await message.edit_text(text=value)
    logger.info('success')

    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info('Dalle3 Started')
    await update.message.reply_text('Напиши текст, по которому сгенерировать изображение: \n'
                                    'Используй /cancel_generation чтобы отменить запрос')

    return RESPONSE


async def response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = await update.effective_message.reply_text('Generating... This can take some time')
    response = await create_image(update.effective_message.text)
    await message.delete()
    await update.effective_message.reply_text(response)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.effective_message.reply_text('Запрос отменён')

    return ConversationHandler.END


async def cancel2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Запрос отменён')

    return ConversationHandler.END


async def secret_access(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info('Secret access requested by user %s', update.effective_user.username)
    await context.bot.set_my_commands(commands=commands, scope=BotCommandScopeChat(chat_id=update.effective_chat.id))
    await update.message.reply_text('Команды добавлены')


async def secret_access_remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info('User %s removed secret access', update.effective_user.username)
    await context.bot.set_my_commands(commands=[], scope=BotCommandScopeChat(chat_id=update.effective_chat.id))
    await update.message.reply_text('Доступ убран')