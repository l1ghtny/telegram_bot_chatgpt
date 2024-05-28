from telegram import Update
from telegram.ext import ContextTypes

from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


async def start_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="*Что опять непонятно?*", parse_mode="MarkdownV2")
