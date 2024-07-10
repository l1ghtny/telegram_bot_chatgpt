from telegram import BotCommand

start = BotCommand(command='start', description='Начать работу с ботом')
dalle_start = BotCommand(command='start_dalle', description='Сгенерировать изображение')
gpt_start = BotCommand(command='ask', description='Задать вопрос ChatGPT4')
subscribe = BotCommand(command='subscribe', description='Оформить подписку')
unsubcribe = BotCommand(command='unsubscribe', description='Отменить подписку')
payment_plans = BotCommand(command='payment_plans', description='Посмотреть варианты подписки')

commands = [start, subscribe, gpt_start, dalle_start, unsubcribe, payment_plans]
