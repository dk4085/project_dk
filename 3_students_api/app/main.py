from fastapi import FastAPI
from sqlalchemy import create_engine
from .database import engine, Base
from .api.endpoints import router
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Создание приложения FastAPI
app = FastAPI(
    title="Students API",
    description="API для управления студентами и группами",
    version="1.0.0"
)

# Подключение роутера с эндпоинтами
app.include_router(router)

@app.get("/", tags=["Корневой эндпоинт"])
def read_root():
    """
    Корневой эндпоинт для проверки работы API.
    """
    return {
        "message": "Добро пожаловать в Students API!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.on_event("startup")
def startup_event():
    """
    Событие запуска приложения.
    """
    print("Students API запущен!")

@app.on_event("shutdown")
def shutdown_event():
    """
    Событие остановки приложения.
    """
    print("Students API остановлен!")