from credentials import terminal_pass
from fast_api_payments.models.payments_models import Payment


async def check_token(data: Payment) -> bool:
    token = data.Token
    created_token = await create_token(data)
    print(token)
    print(created_token)
    if token != created_token:
        return False
    else:
        return True


async def create_token(data: Payment) -> str:
    data_dict = data.model_dump(exclude_none=True)
    data_dict.update({'Password': terminal_pass})
    sorted_items = sorted(data_dict.items())
    values_string = ''.join(str(value) for _, value in sorted_items)
    return values_string

