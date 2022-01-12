from http import HTTPStatus

from app.tests.base_auth_test_case import BaseAuthTestCase


class HistoryTestCase(BaseAuthTestCase):
    url = "/api/v1/user/history"

    def setUp(self):
        super().setUp()
        self.authorize_client()

    def test_get_history(self):
        """
        В тесте проверяется получение истории входов пользователя в аккаунт.
        Т.к. пользователь входил 1 раз при self.authorize_client(), история должна содержать 1 запись.
        """
        response = self.client.get(self.url, headers=self.headers)
        assert response.status_code == HTTPStatus.OK
        events = response.json["events"]
        assert len(events) == 1
        assert events[0].get("user_id") == str(self.user.id)
