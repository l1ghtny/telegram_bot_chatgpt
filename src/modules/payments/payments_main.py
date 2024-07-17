import hashlib

from credentials import terminal_key, terminal_pass
from src.modules.database.operations.payments import get_payment_plan


async def payment_init(user_id, payment_id, description, email, phone):
    current_payment_plan = await get_payment_plan(user_tg_id=user_id, user_uuid=None, payment_plan_id=None)
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
                    "Name": "Наименование товара 1",
                    "Price": 10000,
                    "Quantity": 1,
                    "Amount": 10000,
                    "Tax": "vat10",
                    "Ean13": "303130323930303030630333435"
                },
                {
                    "Name": "Наименование товара 2",
                    "Price": 3500,
                    "Quantity": 2,
                    "Amount": 7000,
                    "Tax": "vat20"
                },
                {
                    "Name": "Наименование товара 3",
                    "Price": 550,
                    "Quantity": 4,
                    "Amount": 4200,
                    "Tax": "vat10"
                }
            ]
        }
    }
