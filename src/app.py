import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

from credentials import bot_token
from src.commands.ru.misc.misc_commands import start_main
from src.commands.ru.openai_commands.openai_commands import secret_access, check_for_gpt_question, secret_access_remove, \
    start2, response2, ASKED, cancel2, RESPONSE, response, start, cancel

from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


def main() -> None:
    application = Application.builder().token(bot_token).build()

    start_handler = CommandHandler('start', start_main)
    secret_handler = CommandHandler('secret_access', secret_access)
    mention_handler = MessageHandler(filters.TEXT, check_for_gpt_question)
    remove_handler = CommandHandler('secret_access_remove', secret_access_remove)
    gpt_handler = ConversationHandler(
        entry_points=[CommandHandler("ask", start2)],
        states={
            ASKED: [
                MessageHandler(filters.TEXT, response2)
            ],
        },
        fallbacks=[CommandHandler("cancel_chat", cancel2)],
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start_dalle", start)],
        states={
            RESPONSE: [
                MessageHandler(filters.TEXT, response)
            ],
        },
        fallbacks=[CommandHandler("cancel_generation", cancel)],
    )

    application.add_handler(secret_handler)
    application.add_handler(remove_handler)
    application.add_handler(conv_handler)
    application.add_handler(gpt_handler)
    application.add_handler(start_handler)
    application.add_handler(mention_handler)

    logger.info(f'bot started at {datetime.datetime.now()}')

    application.run_polling(allowed_updates=Update.ALL_TYPES)
