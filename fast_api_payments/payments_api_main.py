from fastapi import FastAPI

from fast_api_payments.routes.payment_status import payments

app = FastAPI(title="Payments API", version="0.2.1")

app.include_router(payments)


@app.post('/', status_code=200)
async def default() -> str:
    response = 'OK'
    return response
