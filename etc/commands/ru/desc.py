from telegram import BotCommand

start = BotCommand(command='start', description='начать работу с ботом')
dalle_start = BotCommand(command='start_dalle', description='Сгенерировать изображение')
gpt_start = BotCommand(command='ask', description='Задать вопрос ChatGPT4')

commands = [start, gpt_start, dalle_start]