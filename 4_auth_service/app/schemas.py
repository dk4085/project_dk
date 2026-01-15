# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# 注意：这里将 EmailStr 改为 str，避免需要 email-validator
class UserCreate(BaseModel):
    email: str  # 第8行，冒号后面必须有类型
    password: str


class UserLogin(BaseModel):
    email: str  # 同样改为 str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefresh(BaseModel):
    refresh_token: str


class UserUpdate(BaseModel):
    email: Optional[str] = None  # 这里也改为 str
    password: Optional[str] = None


class LoginHistoryOut(BaseModel):
    id: int
    user_id: int
    user_agent: Optional[str]
    datetime: datetime

    class Config:
        orm_mode = True