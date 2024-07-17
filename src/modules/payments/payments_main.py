import hashlib

from credentials import terminal_key, terminal_pass, notification_url
from src.modules.database.operations.payments import get_payment_plan
from src.modules.database.sql_models import Users


async def payment_init(user: Users, payment_id, description, email, phone):
    current_payment_plan = await get_payment_plan(user_tg_id=user.tg_id, user_uuid=None, payment_plan_id=None)
    # здесь надо прописать завершение функции на случай, если клиент всё ещё на бесплатном плане
    amount = current_payment_plan.price_rub
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
