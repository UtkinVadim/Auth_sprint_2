from http import HTTPStatus

from app.models import Role, UserRole
from app.tests.base_auth_test_case import BaseAuthTestCase


class RoleManipulationTestCase(BaseAuthTestCase):
    url = "/api/v1/user/role"

    def setUp(self):
        super().setUp()
        self.authorize_client()

    def test_add_role(self):
        """
        В тесте делается запрос на добавление пользователю роли.
        Проверяется, что после запроса роль появилась у пользователя.
        """
        new_user = self.create_new_user()
        role = Role.create(title="you_awesome")
        data = {"user_id": new_user.id, "role_id": role.id}
        response = self.client.post(self.url, headers=self.headers, json=data)
        assert response.status_code == HTTPStatus.OK
        expected_response = {"message": "role added"}
        assert response.json == expected_response
        assert role in new_user.roles

    def test_remove_role(self):
        """
        В тесте делается запрос на удаление роли пользователя.
        Проверяется, что после запроса роль удалилась у пользователя.
        """
        new_user = self.create_new_user()
        role = Role.create(title="you_awesome")
        UserRole.add(new_user.id, role.id)
        assert role in new_user.roles
        data = {"user_id": new_user.id, "role_id": role.id}
        response = self.client.delete(self.url, headers=self.headers, json=data)
        assert response.status_code == HTTPStatus.OK
        expected_response = {"message": "role deleted"}
        assert response.json == expected_response
        assert role not in new_user.roles
