from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionHistoryResponse, BalanceResponse
from app.services.transaction import TransactionService
from app.repositories.transaction import TransactionRepository
from app.api.routes.user import get_current_user
from app.schemas.user import UserResponse
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


async def get_transaction_service(db: AsyncSession = Depends(get_db)) -> TransactionService:
    transaction_repository = TransactionRepository(db)
    return TransactionService(transaction_repository)


@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: UserResponse = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_transaction_service)
):
    return await transaction_service.create_transaction(current_user.id, transaction_data)


@router.get("/transactions", response_model=List[TransactionHistoryResponse])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    current_user: UserResponse = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_transaction_service)
):
    return await transaction_service.get_user_transactions(current_user.id, skip, limit)


@router.get("/balance", response_model=BalanceResponse)
async def get_balance(
    current_user: UserResponse = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_transaction_service)
):
    return await transaction_service.get_balance(current_user.id)
