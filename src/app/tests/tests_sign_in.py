from http import HTTPStatus

from flask_jwt_extended import get_jti

from app.models import User
from app.tests.base_auth_test_case import BaseAuthTestCase
from app.tests.testing_data import USER_DATA


class SignInTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(self.sign_up_url, json=USER_DATA)

    def test_user_sign_in(self):
        """
        В тесте делается запрос на вход в сервис с логином и паролем.
        Проверяется, что запрос прошел успешно, и вернулись токены.
        """
        response = self.client.post(self.sign_in_url, json=USER_DATA)
        assert response.status_code == HTTPStatus.OK
        assert "access_token" in response.json
        assert "refresh_token" in response.json

    def test_wrong_sign_in_data(self):
        """
        В тесте делается запрос на вход в сервис с логином и неверным паролем.
        Проверяется, что запрос возвращает ошибку.
        """
        data = {"login": "fake_login", "password": "fake_password"}
        response = self.client.post(self.sign_in_url, json=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        expected_details = {"message": "invalid credentials"}
        assert response.json == expected_details

    def test_check_token_in_redis(self):
        """
        В тесте проверяется сохранение токена пользователя в redis после входа.
        """
        self.clear_redis_cache()
        response = self.client.post(self.sign_in_url, json=USER_DATA)
        assert response.status_code == HTTPStatus.OK
        user = User.query.filter_by(login=USER_DATA.get("login")).first()
        refresh_token = response.json["refresh_token"]
        jti = get_jti(refresh_token)
        redis_key = f"{user.id}::{jti}"
        result = self.get_token_from_redis(redis_key)
        assert result == refresh_token
