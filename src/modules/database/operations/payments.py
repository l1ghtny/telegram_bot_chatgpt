from sqlmodel import select

from src.modules.database.sql_model_main import get_session
from src.modules.database.sql_models import PaymentPlans, Users


async def get_payment_plan_rub(id, user_tg_id, user_uuid):
    if id:
        for session in get_session():
            query = select(PaymentPlans).where(PaymentPlans.id == id)
    elif user_tg_id:
        for session in get_session():
            query = select(Users).where(Users.tg_id == user_tg_id)
    elif user_uuid:
        for session in get_session():
            query = select(Users).where(Users.uuid == user_uuid)

