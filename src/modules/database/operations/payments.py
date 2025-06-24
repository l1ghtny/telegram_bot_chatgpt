import logging
import uuid
from sqlmodel import select, update

from src.modules.database.sql_model_main import get_session
from src.modules.database.sql_models import PaymentPlan, Users, Payments
from src.modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


async def get_payment_plan(payment_plan_id, user_tg_id, user_uuid) -> PaymentPlan:
    try:
        if payment_plan_id:
            query = select(PaymentPlan).where(PaymentPlan.id == payment_plan_id)
        elif user_tg_id:
            query = select(PaymentPlan).join(Users).where(Users.tg_id == user_tg_id)
        elif user_uuid:
            query = select(PaymentPlan).where(Users.uuid == user_uuid)
        for session in get_session():
            result = session.execute(query)
            payment_plan = result.first()
            return payment_plan[0]
    except Exception as e:
        logger.error(e)


async def add_payment_plan(payment_plan: PaymentPlan) -> PaymentPlan.id:
    for session in get_session():
        results = session.exec(select(PaymentPlan).order_by(PaymentPlan.id)).all()
        if results:
            latest_plan = results[-1]
            new_id = latest_plan.id+1
        else:
            new_id = 1
        payment_plan.id = new_id
        session.add(payment_plan)
        session.commit()
        return payment_plan.id


async def add_payment(payment: Payments) -> Payments.uuid:
    for session in get_session():
        payment.uuid = str(uuid.uuid4())
        session.add(payment)
        session.commit()
        return payment.uuid


async def update_payment_status(payment_id: str, status: str) -> Payments.uuid:
    for session in get_session():
        payment = session.exec(update(Payments).where(Payments.uuid == payment_id).values(status=status)).first()
        session.commit()
        return payment[0].uuid
