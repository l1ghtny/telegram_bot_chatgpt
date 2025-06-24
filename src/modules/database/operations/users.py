import uuid
from sqlmodel import select

from src.modules.database.sql_model_main import get_session
from src.modules.database.sql_models import Users, Payments


async def add_user(user_id, payment_plan_id, country_id, tg_tag):
    user = Users(tg_id=user_id, payment_plan_id=payment_plan_id, language=country_id, uuid=uuid.uuid4(), tg_tag=tg_tag)
    for session in get_session():
        session.add(user)
        session.commit()


async def add_payment(uu_id, created_at, currency, service, user_id, amount):
    payment = Payments(uuid=uu_id, created_at=created_at, currency=currency, service=service, user_id=user_id, amount=amount)
    for session in get_session():
        session.add(payment)
        session.commit()


async def check_user_exists(user_id):
    for session in get_session():
        query = select(Users).where(Users.tg_id == user_id)
        result = session.exec(query)
        user = result.first()
        exists = bool(user)
        return exists


# async def revert_payment(user_id, payment_id):
#     for session in get_session():
#         query = select(Payments).where(Payments.uuid == payment_id)
#         result = session.exec(query)
#         payment = result.first()
#         return payment[0]


async def get_user_by_tg_id(user_id):
    for session in get_session():
        query = select(Users).where(Users.tg_id == user_id)
        result = session.exec(query)
        user = result.first()
        return user
