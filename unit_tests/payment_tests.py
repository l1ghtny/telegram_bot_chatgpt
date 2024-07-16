import unittest

from src.modules.database.operations.payments import add_payment_plan, get_payment_plan
from src.modules.database.sql_models import PaymentPlan


class PaymentTests(unittest.IsolatedAsyncioTestCase):
    plan: None

    def setUp(self):
        self.addTypeEqualityFunc(PaymentPlan, lambda x, y, msg=None: x.id == y.id and x.name == y.name and x.price_eur == y.price_eur and x.price_rub == y.price_rub and x.price_usd == y.price_usd and x.active == y.active and x.gpt_allowed == y.gpt_allowed and x.images_allowed == y.images_allowed)
    async def test_payment_plans_add(self):
        test_payment_plan = PaymentPlan(
            id=None,
            name='test_plan',
            price_usd=5.06,
            price_eur=4.05,
            price_rub=400,
            active=True,
            gpt_allowed=100,
            images_allowed=10
        )
        PaymentTests.plan = test_payment_plan
        plan_id = await add_payment_plan(test_payment_plan)
        PaymentTests.plan.id = plan_id

    async def test_payment_plans_get_by_id(self):
        payment_plan = await get_payment_plan(payment_plan_id=PaymentTests.plan.id, user_tg_id=None, user_uuid=None)
        self.assertEqual(payment_plan, PaymentTests.plan)
