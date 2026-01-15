# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from models import User, LoginHistory
from schemas import UserUpdate, LoginHistoryOut
from utils import get_password_hash

router = APIRouter(prefix="/user", tags=["user"])


@router.put("/update")
def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Обновление email или пароля пользователя"""
    if user_update.email is not None:
        # Проверка, не занят ли email другим пользователем
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        current_user.email = user_update.email
    if user_update.password is not None:
        current_user.hashed_password = get_password_hash(user_update.password)
    db.commit()
    return {"message": "User updated successfully"}


@router.get("/history", response_model=list[LoginHistoryOut])
def get_login_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Получение истории входов пользователя"""
    history = db.query(LoginHistory).filter(LoginHistory.user_id == current_user.id).order_by(LoginHistory.datetime.desc()).all()
    return history