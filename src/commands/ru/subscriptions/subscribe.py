from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler

from src.commands.ru.commands_text_ru import start_custom_keyboard_3_ru
from src.commands.ru.menu.menu_main import build_menu
from src.commands.ru.menu.payment_buttons import email_phone_list
from src.commands.ru.subscriptions.unsubscribe import unsubscribe_command
from src.modules.chat_bot.misc.actions import send_typing_action
from src.modules.database.operations.users import get_user_by_tg_id
from src.modules.database.sql_models import Users
from src.modules.logs_setup import logger
from src.modules.payments.payments_main import payment_init

logger = logger.logging.getLogger("bot")


EMAIL = 0
PHONE = 1


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
    logger.info('subscribe rf')
    try:
        reply_markup = InlineKeyboardMarkup(await build_menu(email_phone_list, n_cols=2))
    except Exception as e:
        logger.error(e)
    try:
        message = await context.bot.send_message(chat_id=update.effective_chat.id, text='Обрабатываем...', reply_markup=ReplyKeyboardRemove())
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)
        message2 = await context.bot.send_message(chat_id=update.effective_chat.id, text='Предоставьте номер телефона или email для отправки чека', reply_markup=reply_markup)
        context.user_data['message_id'] = message2.id
    except Exception as e:
        logger.error(e)


async def callback_subscribe_3(update: Update, context: CallbackContext):
    await unsubscribe_command(update, context)


async def callback_email(update: Update, context: CallbackContext) -> int:
    logger.info('callback_email')
    try:
        await context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id=context.user_data['message_id'])
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.user_data['message_id'])
        context.user_data.clear()
        await context.bot.send_message(text='Пожалуйста, напишите свой email', chat_id=update.effective_chat.id)
    except Exception as e:
        logger.exception(e)

    return EMAIL


# @send_typing_action
async def callback_pay_tink(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info('Начало оплаты')
    try:
        message = await context.bot.send_message(chat_id=update.effective_chat.id, text='Обрабатываю данные...')
        email = update.message.text
        user = await get_user_by_tg_id(update.effective_user.id)
        link = await payment_init(user, email, None)
        await message.edit_text(f'Ваша ссылка на оплату: {link}')
    except Exception as e:
        logger.exception(e)

    return ConversationHandler.END
