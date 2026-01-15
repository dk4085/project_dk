from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# ==============================================
# SQLite 数据库配置（不需要 PostgreSQL）
# ==============================================
# SQLite 数据库文件将保存在项目根目录
DATABASE_URL = "sqlite:///./students.db"

# SQLite 需要特殊配置（check_same_thread=False）
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии базы данных
def get_db():
    """
    Функция для получения сессии базы данных.
    Используется как зависимость в эндпоинтах.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()