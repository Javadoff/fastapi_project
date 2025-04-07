from typing import Optional, List
from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserInDB, UserResponse
from app.core.security import verify_password


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    async def get_user(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        if await self.user_repository.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        if await self.user_repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user = await self.user_repository.create(user_data)
        return UserResponse.model_validate(user)


    async def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        user = await self.user_repository.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user 