from http import HTTPStatus

from app.models import User
from app.tests.base_auth_test_case import BaseAuthTestCase
from app.tests.testing_data import USER_DATA
from config import SALT


class SignUpTestCase(BaseAuthTestCase):
    def test_create_user(self):
        """
        В тесте делается запрос на создание нового пользователя.
        Проверяется, что пользователь успешно создан и записан в бд.
        """
        response = self.client.post(self.sign_up_url, json=USER_DATA)
        assert response.status_code == HTTPStatus.OK
        assert response.json == {"message": "user created successfully"}

        created_user: User = User.query.filter_by(login=USER_DATA.get("login")).first()

        assert created_user
        assert created_user.login == USER_DATA.get("login")
        assert created_user.email == USER_DATA.get("email")
        assert created_user.password == User.password_hasher(USER_DATA.get("password"), SALT)
