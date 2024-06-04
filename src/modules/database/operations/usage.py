import uuid
from datetime import datetime

from src.constants import gpt4o_input_cost, gpt4o_output_cost
from src.modules.database.operations.users import add_user, check_user_exists
from src.modules.database.sql_model_main import get_session
from src.modules.database.sql_models import GptUsage


async def add_gpt_usage(user_id, tokens_sent, tokens_received):
    user_exists = await check_user_exists(user_id)
    if not user_exists:
        await add_user(user_id, payment_plan_id=1, country_id=1)
    usage_uuid = uuid.uuid4()
    cost_usd = (tokens_sent*gpt4o_input_cost+tokens_received*gpt4o_output_cost)/1000
    gpt_usage = GptUsage(
        request_uuid=usage_uuid,
        request_datetime=datetime.now(),
        user_id=user_id,
        tokens_sent=tokens_sent,
        tokens_received=tokens_received,
        cost_usd=cost_usd
    )
    for session in get_session():
        session.add(gpt_usage)
        session.commit()
