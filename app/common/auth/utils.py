from typing import Optional
from loguru import logger
from lib.factory import get_redis
from lib.utils import get_random_uuid


AUTH_KEY = "auth:%s"


def get_user_id(token: str) -> Optional[str]:
    if token:
        redis = get_redis()
        user_id = redis.get(AUTH_KEY % token)
        if user_id:
            return user_id.decode()


def set_user_id(user_id: str) -> str:
    redis = get_redis()
    token = get_random_uuid()
    redis.set(name=AUTH_KEY % token, value=user_id, ex=86400)
    logger.debug("Saved in redis user:{id}", id=user_id)
    return token


def remove_user_id(token: str):
    redis = get_redis()
    redis.delete(AUTH_KEY % token)
    logger.debug("Removed from redis token:{token}", token=token)
