import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

from credentials import bot_token
from src.commands.admin.payment_plans import add_payment_plan_start, NAME
from src.commands.ru.commands_text_ru import start_custom_keyboard_1_ru
from src.commands.ru.misc.misc_commands import start_main, callback_start_1, callback_start_2, payment_plans
from src.commands.ru.openai_commands.openai_commands import secret_access, check_for_gpt_question, secret_access_remove, \
    start2, response2, ASKED, RESPONSE, response, start, cancel
# from src.commands.ru.subscriptions.subscribe import subscribe, callback_subscribe_1, callback_subscribe_rf, \
#     callback_subscribe_3, callback_pay_tink, callback_email, EMAIL
from src.commands.ru.subscriptions.unsubscribe import unsubscribe_command
from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")

# TODO:
#  0 Finish designing the database
#  0 Add requests to database
#  2. Get subscription check into the gpt commands
#  3. Mock analysis commands
#  4. Create admin role with different menu
#  5. Add database to docker image


def main() -> None:
    application = Application.builder().token(bot_token).concurrent_updates(True).build()
    start_handler = CommandHandler('start', start_main)
    secret_handler = CommandHandler('secret_access', secret_access)
    buttons_start_1 = MessageHandler(filters.Text(start_custom_keyboard_1_ru[0]), callback_start_1)
    buttons_start_2 = MessageHandler(filters.Text(start_custom_keyboard_1_ru[1]), callback_start_2)
    # buttons_subcribe = CommandHandler(command='subscribe', callback=subscribe)
    # buttons_subscribe_1 = MessageHandler(filters.Text(start_custom_keyboard_3_ru[0]), callback_subscribe_1)
    # buttons_subscribe_2 = MessageHandler(filters.Text(start_custom_keyboard_3_ru[1]), callback_subscribe_rf)
    # buttons_subcribe_3 = MessageHandler(filters.Text(start_custom_keyboard_3_ru[2]), callback_subscribe_3)
    unsubscribe = CommandHandler('unsubscribe', unsubscribe_command)
    payment_plans_command = CommandHandler('payment_plans', payment_plans)
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
        fallbacks=[CommandHandler("cancel_chat", cancel)],
    )
    add_payment_plan_handler = ConversationHandler(
        name='add_payment_plan',
        entry_points=[CommandHandler("add_payment_plan", add_payment_plan_start)],
        states={
            NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_payment_plan_start)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    # callback_phone_handler = CallbackQueryHandler(callback=callback_pay_tink, pattern=email_phone_list[0].callback_data)
    # callback_email_handler = ConversationHandler(
    #     name='callback_email',
    #     entry_points=[CallbackQueryHandler(callback=callback_email, pattern=email_phone_list[1].callback_data)],
    #     states={
    #         EMAIL: [
    #             MessageHandler(filters.TEXT & ~filters.COMMAND, callback_pay_tink)
    #         ],
    #     },
    #     fallbacks=[CommandHandler("cancel", cancel)],
    # )
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
    application.add_handlers(
        [
            start_handler,
            # buttons_subscribe_2,
            buttons_start_1,
            buttons_start_2,
            # callback_email_handler,
            # buttons_subcribe,
            # buttons_subscribe_1,
            # buttons_subcribe_3,
            unsubscribe,
            payment_plans_command])
    application.add_handlers([secret_handler, remove_handler, mention_handler])

    logger.info(f'gpt bot started at {datetime.datetime.now()}')
    application.run_polling(allowed_updates=Update.ALL_TYPES)
