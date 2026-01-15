# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
from dependencies import get_db
from models import User, LoginHistory
from schemas import UserCreate, UserLogin, Token, TokenRefresh
from utils import verify_password, get_password_hash, create_access_token, create_refresh_token, verify_token
from redis_client import add_to_blacklist
from fastapi.security import HTTPBearer
import os

router = APIRouter(prefix="", tags=["auth"])
security = HTTPBearer()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    # Проверка, существует ли пользователь с таким email
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    # Хеширование пароля и создание пользователя
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Создание токенов
    access_token = create_access_token(data={"sub": str(new_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(new_user.id)})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/login", response_model=Token)
def login(user: UserLogin, request: Request, db: Session = Depends(get_db)):
    """Авторизация пользователя"""
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    # Запись истории входа
    user_agent = request.headers.get("User-Agent")
    login_history = LoginHistory(user_id=db_user.id, user_agent=user_agent)
    db.add(login_history)
    db.commit()
    # Создание токенов
    access_token = create_access_token(data={"sub": str(db_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id)})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh", response_model=Token)
def refresh(token: TokenRefresh):
    """Обновление access токена с помощью refresh токена"""
    refresh_token = token.refresh_token
    payload = verify_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user_id = payload.get("sub")
    # Создание нового access токена
    access_token = create_access_token(data={"sub": user_id})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/logout")
def logout(access_token: str = Depends(security)):
    """Выход из системы - добавление access токена в черный список"""
    token = access_token.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # Проверяем, что это access токен
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not an access token")
    # Добавляем токен в черный список до истечения его срока действия
    exp = payload.get("exp")
    if exp:
        current_time = datetime.utcnow().timestamp()
        expire_seconds = int(exp - current_time)
        if expire_seconds > 0:
            add_to_blacklist(token, expire_seconds)
    return {"message": "Successfully logged out"}