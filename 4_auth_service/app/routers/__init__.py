# app/routers/__init__.py
"""
Роутеры API для Auth-сервиса
"""

from .auth import router as auth_router
from .user import router as user_router

# Экспорт роутеров для удобного импорта
__all__ = ["auth_router", "user_router"]