from datetime import datetime
from typing import Optional

from flask_jwt_extended import get_jti
from flask_testing import TestCase

from app import create_app, db, jwt, redis_client
from app.models import Role, User, UserRole
from app.tests.testing_data import USER_DATA
from config import (
    TEST_DB,
    TEST_DB_HOST,
    TEST_DB_PASSWORD,
    TEST_DB_PORT,
    TEST_DB_USER,
    TEST_REDIS_DB
)


class BaseAuthTestCase(TestCase):
    SQLALCHEMY_DATABASE_URI = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB}"
    TESTING = True

    sign_up_url = "/api/user/sign_up"
    sign_in_url = "/api/user/sign_in"
    sign_out_url = "/api/user/sign_out"

    def create_app(self):
        """
        Метод для создания тестового приложения.
        """
        test_config = {
            "SQLALCHEMY_DATABASE_URI": self.SQLALCHEMY_DATABASE_URI,
            "TESTING": True,
        }
        app = create_app(test_config)
        jwt.init_app(app)
        return app

    def setUp(self):
        self.db = db
        self.redis_client = redis_client.db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.clear_redis_cache()

    def clear_redis_cache(self):
        """
        Метод для удаления всех тестовых данных из redis.
        """
        if keys := self.redis_client.keys("*"):
            self.redis_client.delete(*keys)

    def authorize_client(self):
        """
        Метод для создания юзера с правами администратора.
        """
        self.client.post(self.sign_up_url, json=USER_DATA)
        self.user = User.query.filter_by(login=USER_DATA.get("login")).first()
        self.role = Role.create(title="admin")
        UserRole.add(self.user.id, self.role.id)
        response = self.client.post(self.sign_in_url, json=USER_DATA)
        self.access_token = response.json["access_token"]
        self.refresh_token = response.json["refresh_token"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.headers_refresh = {"Authorization": f"Bearer {self.refresh_token}"}

    def create_new_user(self, login: str = None, password: str = None, email: str = None) -> User:
        """
        Метод, для создания нового юзера.
        """
        login = login if login else f"user_{datetime.now().timestamp()}"
        password = password if password else login
        email = email if email else f"{login}@{login}.com"
        user_data = {"login": login, "password": password, "email": email}
        self.client.post(self.sign_up_url, json=user_data)
        return User.query.filter_by(login=login).first()

    def get_token_from_redis(self, redis_key: str = None) -> Optional[str]:
        """
        Метод для получения токена из redis.
        Можно получить передав ключ, либо ключ будет сконфигурирован автоматически, если в тесте был вызван метод
        authorize_client()
        """
        if redis_key:
            return self.redis_client.get(redis_key)
        jti = get_jti(self.refresh_token)
        redis_key = f"{self.user.id}::{jti}"
        return self.redis_client.get(redis_key)
