import datetime
from pprint import pprint

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

from credentials import bot_token
from src.commands.ru.misc.misc_commands import start_main
from src.commands.ru.openai_commands.openai_commands import secret_access, check_for_gpt_question, secret_access_remove, \
    start2, response2, ASKED, cancel2, RESPONSE, response, start, cancel

from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


# TODO:
#  0.5 Finish designing the database
#  1. Add requests to database
#  2. Get subscription check into the gpt commands
#  3. Mock analysis commands
#  4. Create admin role with different menu
#  5. Add database to docker image


def main() -> None:
    application = Application.builder().token(bot_token).concurrent_updates(True).build()
    start_handler = CommandHandler('start', start_main)
    secret_handler = CommandHandler('secret_access', secret_access)
    mention_handler = MessageHandler(filters.TEXT, check_for_gpt_question)
    remove_handler = CommandHandler('secret_access_remove', secret_access_remove)
    gpt_handler = ConversationHandler(
        name='ask_gpt4',
        entry_points=[CommandHandler("ask", start2)],
        states={
            ASKED: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, response2)
            ],
        },
        fallbacks=[CommandHandler("cancel_chat", cancel2)],
    )

    image_handler = ConversationHandler(
        name='Dalle3',
        entry_points=[CommandHandler("start_dalle", start)],
        states={
            RESPONSE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, response)
            ],
        },
        fallbacks=[CommandHandler("cancel_generation", cancel)],
    )

    application.add_handlers([gpt_handler, image_handler])
    application.add_handlers([secret_handler, remove_handler, start_handler, mention_handler])

    logger.info(f'gpt bot started at {datetime.datetime.now()}')
    logger.info('handlers: \n %s', application.handlers.items())
    application.run_polling(allowed_updates=Update.ALL_TYPES)
