from http import HTTPStatus

from app.models import SocialAccount
from app.tests.base_auth_test_case import BaseAuthTestCase


class RemoveSocialAccountTestCase(BaseAuthTestCase):
    url = "/api/remove_social_account"

    def setUp(self):
        super().setUp()
        self.authorize_client()
        self.social_name = "vk"

    def test_remove_social_account(self):
        """
        В тесте проверяется открепление аккаунта в социальном сервисе от пользователя.
        """
        SocialAccount.create_social_connect(social_id="fake_id", social_name=self.social_name, user_id=self.user.id)
        data = {"social_name": self.social_name}
        response = self.client.post(self.url, headers=self.headers, json=data)
        assert response.status_code == HTTPStatus.OK
        social_account = SocialAccount.query.filter_by(user_id=self.user.id).one_or_none()
        assert not social_account

    def test_social_account_not_exists(self):
        """
        В тесте проверяется открепление не привязанного к пользователю аккаунта.
        """
        data = {"social_name": "fake_name"}
        response = self.client.post(self.url, headers=self.headers, json=data)
        assert response.status_code == HTTPStatus.CONFLICT
        expected_response = {"message": "no social account"}
        assert response.json == expected_response
