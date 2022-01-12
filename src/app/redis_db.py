from flask_jwt_extended import get_jti
import redis

from config import JWT_REFRESH_TOKEN_EXPIRES


class RedisConnector:
    def __init__(self, redis_host, redis_port, redis_db=0, **kwargs):
        self.db = redis.Redis(host=redis_host, port=redis_port, db=redis_db, **kwargs, decode_responses=True)

    def set_user_refresh_token(self, user_id: str, refresh_token: str) -> None:
        """
        Метод, для записи токена пользователя.
        """
        jti = get_jti(refresh_token)
        key = self.generate_redis_key(user_id, jti)
        self.db.set(key, refresh_token, ex=JWT_REFRESH_TOKEN_EXPIRES)

    def refresh_user_token(self, user_id: str, old_jwt: dict, new_jwt: str):
        """
        Метод для обновления токена пользователя.
        """
        self.remove_user_token(old_jwt)
        self.set_user_refresh_token(user_id, new_jwt)

    def remove_user_token(self, refresh_token: dict) -> None:
        """
        Метод для удаления токена пользователя.
        """
        jti = refresh_token["jti"]
        user_id = refresh_token["sub"]
        key = self.generate_redis_key(user_id, jti)
        self.db.delete(key)

    def remove_all_user_tokens(self, refresh_token: dict) -> None:
        """
        Метод для удаления всех токенов принадлежащих пользователю.
        """
        user_id = refresh_token["sub"]
        if keys := self.db.keys(f"{user_id}::*"):
            self.db.delete(*keys)

    def token_is_revoked(self, user_id: str, jti: str) -> bool:
        """
        Метод для проверки токена пользователя на наличие в redis.
        """
        key = self.generate_redis_key(user_id, jti)
        result = self.db.get(key)
        if not result:
            return True
        return False

    @staticmethod
    def generate_redis_key(user_id: str, jti: str) -> str:
        """
        Метод для генерации ключа для redis.
        """
        return "::".join([user_id, jti])


