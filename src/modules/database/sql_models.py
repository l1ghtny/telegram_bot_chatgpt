from datetime import datetime
from typing import Optional

from sqlalchemy import TEXT
from sqlmodel import SQLModel, Field, Relationship, SMALLINT

SQLModel.model_config.update(arbitrary_types_allowed=True)


class Users(SQLModel, table=True):
    # __table_args__ = {'schema': 'public'}  # Specify the custom schema here

    tg_id: int = Field(default=None, primary_key=True)
    payment_plan_id: int = Field(SMALLINT)
    language: int = Field(TEXT)
    payments: Optional[list['Payments']] = Relationship(back_populates="user")
    gpt_usage: Optional[list['GptUsage']] = Relationship(back_populates="user")
    image_usage: Optional[list['ImageUsage']] = Relationship(back_populates="user")


class Payments(SQLModel, table=True):
    # __table_args__ = {'schema': 'public'}  # Specify the custom schema here

    uuid: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    currency: int = Field(nullable=False)
    amount: float = Field(nullable=False)
    service: int = Field(nullable=False)
    user_id: int = Field(foreign_key='users.tg_id')
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


class PaymentPlans(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    price_usd: float = Field(nullable=False)
    price_eur: float = Field(nullable=False)
    price_rub: float = Field(nullable=False)
    active: bool = Field(nullable=False)
