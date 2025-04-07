from typing import Optional, List
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import users
from app.schemas.user import UserCreate, UserUpdate, UserInDB
from app.core.security import get_password_hash


class UserRepository:
    def __init__(self, database: AsyncSession):
        self.db = database

    async def get_by_id(self, user_id: int) -> Optional[UserInDB]:
        query = select(users).where(users.c.id == user_id)
        result = await self.db.execute(query)
        user = result.first()
        if user:
            return UserInDB.model_validate({k: v for k, v in user._mapping.items()})
        return None

    async def get_by_username(self, username: str) -> Optional[UserInDB]:
        query = select(users).where(users.c.username == username)
        result = await self.db.execute(query)
        user = result.first()
        if user:
            return UserInDB.model_validate({k: v for k, v in user._mapping.items()})
        return None

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        query = select(users).where(users.c.email == email)
        result = await self.db.execute(query)
        user = result.first()
        if user:
            return UserInDB.model_validate({k: v for k, v in user._mapping.items()})
        return None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserInDB]:
        query = select(users).offset(skip).limit(limit)
        result = await self.db.execute(query)
        users_data = result.all()
        return [UserInDB.model_validate({k: v for k, v in user._mapping.items()}) for user in users_data]

    async def create(self, user_data: UserCreate) -> UserInDB:
        hashed_password = get_password_hash(user_data.password)
        query = insert(users).values(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        ).returning(users)
        result = await self.db.execute(query)
        await self.db.commit()
        user = result.first()
        return UserInDB.model_validate({k: v for k, v in user._mapping.items()})

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserInDB]:
        update_data = user_data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
        if update_data:
            query = update(users).where(users.c.id == user_id).values(update_data).returning(users)
            result = await self.db.execute(query)
            await self.db.commit()
            user = result.first()
            if user:
                return UserInDB.model_validate({k: v for k, v in user._mapping.items()})
        
        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> bool:
        query = delete(users).where(users.c.id == user_id)
        await self.db.execute(query)
        await self.db.commit()
        return True 