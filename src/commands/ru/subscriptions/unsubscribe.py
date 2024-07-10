from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Эта команда станет доступна после подключения оплаты. \n\nПри отмене '
                                            'подписки следующая оплата не списывается, доступ к командам сохраняется '
                                            'на остаток оплаченного периода', reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        logger.error(e)
