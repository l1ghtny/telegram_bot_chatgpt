from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, CallbackContext

from src.commands.ru.commands_text_ru import start_custom_keyboard_1_ru, start_message_text_ru, start_message_text_2_ru, \
    start_message_text_3_ru
from src.commands.ru.openai_commands.openai_commands import secret_access
from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


async def start_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = ReplyKeyboardMarkup([start_custom_keyboard_1_ru])
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=reply_markup,
                                       text=start_message_text_ru)
    except Exception as e:
        logger.error(e)


async def callback_start_1(update: Update, context: CallbackContext):
    await secret_access(update, context)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message_text_2_ru, reply_markup=ReplyKeyboardRemove())


async def callback_start_2(update: Update, context: CallbackContext):
    await secret_access(update, context)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message_text_3_ru, reply_markup=ReplyKeyboardRemove())


async def payment_plans(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message_text_3_ru)
