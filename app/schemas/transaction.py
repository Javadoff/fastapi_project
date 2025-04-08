from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, Literal
from decimal import Decimal


class TransactionBase(BaseModel):
    amount: Decimal = Field(..., description="Transaction amount", decimal_places=2)
    currency: Literal["USD", "EUR", "GBP"] = Field(..., description="Transaction currency")
    transaction_type: Literal["deposit", "withdrawal"] = Field(..., description="Type of transaction")
    recipient_id: Optional[int] = Field(None, description="Recipient user ID for transfers")


class TransactionCreate(TransactionBase):
    pass


class TransactionInDB(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: Literal["pending", "success", "failed"]
    timestamp: datetime


class TransactionResponse(BaseModel):
    transaction_id: int
    status: Literal["pending", "success", "failed"]


class TransactionHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transaction_id: int
    amount: Decimal
    currency: str
    transaction_type: str
    recipient_id: Optional[int]
    status: str
    timestamp: datetime


class BalanceResponse(BaseModel):
    user_id: int
    balance: Decimal
    currency: str


