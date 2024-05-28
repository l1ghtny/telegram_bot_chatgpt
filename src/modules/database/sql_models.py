from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import SQLModel, Field, Relationship, SMALLINT

SQLModel.model_config.update(arbitrary_types_allowed=True)


class Users(SQLModel, table=True):
    # __table_args__ = {'schema': 'public'}  # Specify the custom schema here

    id: int = Field(default=None, primary_key=True)
    payment_plan_id: int = Field(SMALLINT)
    country_id: int = Field(SMALLINT)
    payments: Optional[list['Payments']] = Relationship(back_populates="user")


class Payments(SQLModel, table=True):
    # __table_args__ = {'schema': 'public'}  # Specify the custom schema here

    uuid: str = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    currency: int = Field(nullable=False)
    amount: float = Field(nullable=False)
    service: int = Field(nullable=False)
    user_id: int = Field(foreign_key='users.id')
    user: 'Users' = Relationship(back_populates="payments")
