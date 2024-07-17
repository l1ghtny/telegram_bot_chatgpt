from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from src.commands.ru.commands_text_ru import start_custom_keyboard_3_ru
from src.commands.ru.menu.menu_main import build_menu
from src.commands.ru.menu.payment_buttons import email_phone_list
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
    reply_markup = InlineKeyboardMarkup(await build_menu(email_phone_list, n_cols=2))
    try:
        message = await context.bot.send_message(chat_id=update.effective_chat.id, text='Обрабатываем...', reply_markup=ReplyKeyboardRemove())
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Предоставьте номер телефона или email для отправки чека', reply_markup=reply_markup)
    except Exception as e:
        logger.error(e)


async def callback_subscribe_3(update: Update, context: CallbackContext):
    await unsubscribe_command(update, context)


async def callback_email(update: Update, context: CallbackContext):
    await context.bot.send_message(text='Пожалуйста, напишите свой email', chat_id=update.effective_chat.id)


async def callback_pay_tink(update: Update, context: CallbackContext):

