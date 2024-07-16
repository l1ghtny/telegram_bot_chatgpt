import hashlib

from credentials import terminal_key, terminal_pass


async def payment_init(user_id, amount, payment_id, description, email, phone):
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
