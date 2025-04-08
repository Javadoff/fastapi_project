from fastapi import HTTPException, status
from typing import List
from app.repositories.transaction import TransactionRepository
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionHistoryResponse,
    BalanceResponse
)
from decimal import Decimal


class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    async def create_transaction(self, user_id: int, transaction_data: TransactionCreate) -> TransactionResponse:
        try:
            amount = Decimal(str(transaction_data.amount))
            transaction_data.amount = amount

            if amount <= Decimal('0'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transaction amount must be positive"
                )

            if transaction_data.transaction_type == "withdrawal":
                current_balance = await self.get_balance(user_id)
                if current_balance.balance < amount:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Insufficient funds"
                    )
                if current_balance.currency != transaction_data.currency:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Currency mismatch"
                    )

            return await self.transaction_repository.create_transaction(user_id, transaction_data)
        except ValueError as ve:
            print(f"Validation error: {ve}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid amount format: {str(ve)}"
            )
        except HTTPException as he:
            print(f"HTTP error: {he.detail}")
            raise he
        except Exception as e:
            print(f"Unexpected error in create_transaction: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process transaction: {str(e)}"
            )

    async def get_user_transactions(self, user_id: int, skip: int = 0, limit: int = 100) -> List[TransactionHistoryResponse]:
        return await self.transaction_repository.get_user_transactions(user_id, skip, limit)

    async def get_balance(self, user_id: int) -> BalanceResponse:
        return await self.transaction_repository.get_user_balance(user_id)
