from telegram import Update
from telegram.ext import CallbackContext


NAME = 0
PRICE_USD = 1
PRICE_EUR = 2
PRICE_RUB = 3
ACTIVE = 4
GPT_ALLOWED = 5
IMAGES_ALLOWED = 6


async def add_payment_plan_start(update: Update, context: CallbackContext):
    await context.bot.send_message('please provide the name for your payment plan')

    return
