from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, CallbackContext

from src.commands.ru.commands_text_ru import start_custom_keyboard_3_ru
from src.commands.ru.subscriptions.unsubscribe import unsubscribe_command
from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = ReplyKeyboardMarkup([start_custom_keyboard_3_ru])
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=reply_markup,
                                       text='Выберите способ оплаты')
    except Exception as e:
        logger.error(e)


async def callback_subscribe_1(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Эта команда станет доступна после подключения оплаты', reply_markup=ReplyKeyboardRemove())


async def callback_subscribe_rf(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Эта команда станет доступна после подключения оплаты', reply_markup=ReplyKeyboardRemove())


async def callback_subscribe_3(update: Update, context: CallbackContext):
    await unsubscribe_command(update, context)
