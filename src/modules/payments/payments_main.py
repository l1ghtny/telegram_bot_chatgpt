import datetime
import hashlib
import json
import requests
from pprint import pprint

from credentials import terminal_key, terminal_pass, notification_url
from src.constants import t_kassa_api_url
from src.modules.database.operations.payments import get_payment_plan, add_payment
from src.modules.database.sql_models import Users, Payments
from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


async def payment_init(user: Users, email, phone):
    try:
        current_payment_plan = await get_payment_plan(user_tg_id=user.tg_id, user_uuid=None, payment_plan_id=None)
    except Exception as e:
        logger.exception(e)
    # здесь надо прописать завершение функции на случай, если клиент всё ещё на бесплатном плане
    amount = int(current_payment_plan.price_rub)
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
    token_data = f"{amount*100}{str(user.uuid)}{current_payment_plan.name}ru{notification_url}{str(payment_id)}{terminal_pass}OY{terminal_key}"
    token = hashlib.sha256(token_data.encode()).hexdigest()
    print(token_data)
    payment_data = {
        "TerminalKey": terminal_key,
        "Amount": amount*100,
        "OrderId": str(payment_id),
        "Description": current_payment_plan.name,
        "Token": token,
        "CustomerKey": str(user.uuid),
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
    url = f'{t_kassa_api_url}/Init'
    print(url)
    result = requests.post(url=url, json=payment_data, headers={'Content-Type': 'application/json'})
    code = result.status_code
    pprint(code)
    result = result.json()
    print(result)

    return result['PaymentURL']
