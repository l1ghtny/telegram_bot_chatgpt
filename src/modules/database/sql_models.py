import uuid as uuid_pkg
from datetime import datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as UUIDSA
from sqlmodel import SQLModel, Field, Relationship

SQLModel.model_config.update(arbitrary_types_allowed=True)


class Users(SQLModel, table=True):
    tg_id: int = Field(default=None, primary_key=True)
    payment_plan_id: int = Field(foreign_key='payment_plans.id')
    language: int = Field(nullable=False)
    uuid: Optional[uuid_pkg.UUID] = Field(
        sa_column=Column(
            UUIDSA(as_uuid=True),
            primary_key=False,
            index=True,
            nullable=False,
        )
    )
    tg_tag: str = Field(nullable=False)
    payment_plan: 'PaymentPlan' = Relationship(back_populates="user")
    payments: Optional[list['Payments']] = Relationship(back_populates="user")
    gpt_usage: Optional[list['GptUsage']] = Relationship(back_populates="user")
    image_usage: Optional[list['ImageUsage']] = Relationship(back_populates="user")


class Payments(SQLModel, table=True):
    uuid: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    currency: int = Field(nullable=False)
    amount: float = Field(nullable=False)
    service: int = Field(nullable=False)
    user_id: int = Field(foreign_key='users.tg_id')
    status: int = Field(nullable=False)
    user: 'Users' = Relationship(back_populates="payments")


class GptUsage(SQLModel, table=True):
    request_uuid: str = Field(primary_key=True)
    request_datetime: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key='users.tg_id')
    tokens_sent: int = Field(default_factory=int, nullable=False)
    tokens_received: int = Field(default_factory=int, nullable=False)
    cost_usd: float = Field(nullable=False)
    user: 'Users' = Relationship(back_populates="gpt_usage")


class ImageUsage(SQLModel, table=True):
    request_uuid: str = Field(primary_key=True)
    user_id: int = Field(foreign_key='users.tg_id')
    request_datetime: datetime = Field(default_factory=datetime.now)
    cost_usd: float = Field(nullable=False)
    user: 'Users' = Relationship(back_populates="image_usage")


class Currency(SQLModel, table=True):
    id: int = Field(primary_key=True)
    description: str = Field(nullable=False)


class Language(SQLModel, table=True):
    code: int = Field(primary_key=True)
    name: str = Field(nullable=False)


class PaymentPlan(SQLModel, table=True):
    __tablename__ = "payment_plans"
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    price_usd: float = Field(nullable=False)
    price_eur: float = Field(nullable=False)
    price_rub: float = Field(nullable=False)
    active: bool = Field(nullable=False)
    gpt_allowed: int = Field(nullable=False)
    images_allowed: int = Field(nullable=False)
    user: Optional[list['Users']] = Relationship(back_populates="payment_plan")
