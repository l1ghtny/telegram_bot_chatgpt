from src.modules.database.sql_model_main import get_session
from src.modules.database.sql_models import Users, Payments


async def add_user(user_id, payment_plan_id, country_id):
    user = Users(id=user_id, payment_plan_id=payment_plan_id, country_id=country_id)
    for session in get_session():
        session.add(user)
        session.commit()


async def add_payment(uu_id, created_at, currency, service, user_id):
    payment = Payments(uuid=uu_id, created_at=created_at, currency=currency, service=service, user_id=user_id)
    for session in get_session():
        session.add(payment)
        session.commit()


