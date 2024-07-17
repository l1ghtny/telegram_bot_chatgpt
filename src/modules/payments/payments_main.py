import datetime
import hashlib
from pprint import pprint

import requests

from credentials import terminal_key, terminal_pass, notification_url
from src.constants import t_kassa_api_url
from src.modules.database.operations.payments import get_payment_plan, add_payment
from src.modules.database.sql_models import Users, Payments


async def payment_init(user: Users, description, email, phone):
    current_payment_plan = await get_payment_plan(user_tg_id=user.tg_id, user_uuid=None, payment_plan_id=None)
    # здесь надо прописать завершение функции на случай, если клиент всё ещё на бесплатном плане
    amount = current_payment_plan.price_rub
    payment = Payments(
        uuid=None,
        created_at=datetime.datetime.now(),
        currency=3,
        amount=amount,
        user_id=user.tg_id,
        status=0,
        payment_plan=current_payment_plan.id
    )
    payment_id = await add_payment(payment)
    token_data = f"{amount}{description}{payment_id}{terminal_pass}{terminal_key}"
    token = hashlib.sha256(token_data.encode()).hexdigest()
    payment_data = {
        "TerminalKey": terminal_key,
        "Amount": amount,
        "OrderId": payment_id,
        "Description": description,
        "Token": token,
        "CustomerKey": user.uuid,
        "Recurrent": 'Y',
        "PayType": 'O',
        "Language": 'ru',
        "NotificationURL": notification_url,
        "DATA": {
            "Phone": phone,
            "Email": email
        },
        "Receipt": {
            "Email": email,
            "Phone": phone,
            "Taxation": "usn_income",
            "Items": [
                {
                    "Name": current_payment_plan.name,
                    "Price": amount*100,
                    "Quantity": 1,
                    "Amount": amount*100,
                    "Tax": "none",
                    "PaymentObject": 'service'
                }
            ]
        }
    }

    result = requests.post(t_kassa_api_url, data=payment_data, headers={'Content-Type': 'application/json'}).json()
    pprint(result)
