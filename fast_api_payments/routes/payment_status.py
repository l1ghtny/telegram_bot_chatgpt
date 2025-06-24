from fastapi import APIRouter

from fast_api_payments.models.payments_models import Payment
from fast_api_payments.tokenisation_tink import check_token
from src.modules.database.operations.payments import update_payment_status
from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")

payments = APIRouter(prefix='/payments', tags=['payments'])


@payments.post('/tink_payment', status_code=200)
async def send_payment_status(data: Payment) -> str:
    is_token_correct = await check_token(data)
    if is_token_correct and data.Success:
        await update_payment_status(data.PaymentId, 'Success')
    elif is_token_correct and not data.Success:
        await update_payment_status(data.PaymentId, 'Failed')
    elif not is_token_correct:
        logger.error('Token is not correct')
    print(data)
    print('is token correct:', is_token_correct)
    response = 'OK'
    return response
