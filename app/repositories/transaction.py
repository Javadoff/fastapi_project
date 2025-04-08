from typing import Optional, List
from sqlalchemy import select, insert, and_, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import transactions
from app.schemas.transaction import (
    TransactionCreate, 
    TransactionInDB, 
    TransactionResponse, 
    TransactionHistoryResponse,
    BalanceResponse
)
from decimal import Decimal


class TransactionRepository:
    def __init__(self, database: AsyncSession):
        self.db = database

    async def create_transaction(self, user_id: int, transaction_data: TransactionCreate) -> TransactionResponse:
        amount = transaction_data.amount
        if transaction_data.transaction_type == "withdrawal":
            amount = -abs(amount)
        elif transaction_data.transaction_type == "deposit":
            amount = abs(amount)

        query = insert(transactions).values(
            user_id=user_id,
            amount=amount,
            currency=transaction_data.currency,
            transaction_type=transaction_data.transaction_type,
            recipient_id=transaction_data.recipient_id,
            status="pending"
        ).returning(transactions)
        
        result = await self.db.execute(query)
        transaction = result.first()
        
        update_query = text(
            "UPDATE transactions SET status = 'success' WHERE id = :transaction_id"
        )
        await self.db.execute(update_query, {"transaction_id": transaction.id})
        
        await self.db.commit()
        
        return TransactionResponse(
            transaction_id=transaction.id,
            status="success"
        )

    async def get_user_transactions(self, user_id: int, skip: int = 0, limit: int = 100) -> List[TransactionHistoryResponse]:
        query = select(transactions).where(
            transactions.c.user_id == user_id
        ).offset(skip).limit(limit).order_by(transactions.c.timestamp.desc())
        
        result = await self.db.execute(query)
        transactions_data = result.all()
        
        return [
            TransactionHistoryResponse(
                transaction_id=t.id,
                amount=abs(t.amount),
                currency=t.currency,
                transaction_type=t.transaction_type,
                recipient_id=t.recipient_id,
                status=t.status,
                timestamp=t.timestamp
            ) 
            for t in transactions_data
        ]

    async def get_user_balance(self, user_id: int) -> BalanceResponse:
        query = select(
            transactions.c.user_id,
            func.sum(transactions.c.amount).label('balance'),
            transactions.c.currency
        ).where(
            and_(
                transactions.c.user_id == user_id,
                transactions.c.status == 'success'
            )
        ).group_by(
            transactions.c.user_id,
            transactions.c.currency
        )
        
        result = await self.db.execute(query)
        balance_data = result.first()
        
        if not balance_data:
            return BalanceResponse(
                user_id=user_id,
                balance=Decimal('0.00'),
                currency="USD"
            )
        
        return BalanceResponse(
            user_id=balance_data.user_id,
            balance=balance_data.balance or Decimal('0.00'),
            currency=balance_data.currency
        )
