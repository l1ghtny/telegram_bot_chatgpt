from pydantic import BaseModel


class PaymentData(BaseModel):
    Route: str
    Source: str
    CreditAmount: int


class Payment(BaseModel):
    TerminalKey: str
    Amount: int
    OrderId: str
    Success: bool
    PaymentId: str
    ErrorCode: str
    Message: str
    Details: str
    RebillId: int
    CardId: int
    Pan: str
    ExpDate: str
    Token: str
    DATA: PaymentData | None = None
