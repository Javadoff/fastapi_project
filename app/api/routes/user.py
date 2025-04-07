from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin, Token
from app.services.user import UserService 
from app.core.security import create_access_token, verify_password, verify_token
from app.repositories.user import UserRepository
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository)

async def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)) -> UserResponse:
    payload = verify_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    username = payload["sub"]
    user = await user_service.user_repository.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return UserResponse.model_validate(user)

@router.post("/register", response_model=Dict[str, Any])
async def register_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    user = await user_service.create_user(user_data)
    return {
        "message": "User registered successfully",
        "user_id": user.id
    }

@router.post("/login", response_model=Token)
async def login_for_access_token(login_data: UserLogin, user_service: UserService = Depends(get_user_service)):
    user = await user_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


