import uuid

from telegram import InlineKeyboardButton

plans_list = [
    InlineKeyboardButton("pay_test", callback_data=str(uuid.uuid4()))
]

email_phone_list = [
    InlineKeyboardButton("номер", callback_data=str(uuid.uuid4())),
    InlineKeyboardButton('email', callback_data=str(uuid.uuid4()))
]