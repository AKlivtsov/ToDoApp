import redis
from datetime import timedelta

import os
from dotenv import load_dotenv

load_dotenv()
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"), 
    port=os.getenv("REDIS_PORT"), 
    db=0, 
    decode_responses=True
)

def cache_token(user_id: str, token: str, expire_time: int = 86400) -> None:
    """
    Сохраняет токен в Redis с временем жизни
    :param user_id: ID пользователя
    :param token: Токен для кеширования
    :param expire_time: Время жизни в секундах (по умолчанию 24 часа)
    """
    redis_client.set(f"token:{user_id}", token, ex=expire_time)

def get_cached_token(user_id: str) -> str | None:
    """
    Получает токен из Redis по ID пользователя
    :param user_id: ID пользователя
    :return: Токен или None, если не найден
    """
    return redis_client.get(f"token:{user_id}")

def get_cached_user_id(token: str) -> str | None:
    """
    Получает ID пользователя из Redis по токену
    :param token: Токен пользователя
    :return: ID пользователя или None, если не найден
    """
    # Получаем все ключи
    keys = redis_client.keys("token:*")
    
    # Ищем ключ, значение которого соответствует токену
    for key in keys:
        if redis_client.get(key) == token:
            # Возвращаем ID пользователя (убираем префикс "token:")
            return key.replace("token:", "")
    
    return None