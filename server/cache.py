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
    redis_client.set(f"token:{user_id}", token, ex=expire_time)

def get_cached_token(user_id: str) -> str | None:
    return redis_client.get(f"token:{user_id}")

def get_cached_user_id(token: str) -> str | None:
    keys = redis_client.keys("token:*")
    for key in keys:
        if redis_client.get(key) == token:
            return key.replace("token:", "")
    
    return None