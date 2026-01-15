# app/redis_client.py
import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def add_to_blacklist(token: str, expire_seconds: int):
    """Добавление токена в черный список"""
    redis_client.setex(token, expire_seconds, "blacklisted")


def is_blacklisted(token: str) -> bool:
    """Проверка, находится ли токен в черном списке"""
    return redis_client.exists(token) == 1