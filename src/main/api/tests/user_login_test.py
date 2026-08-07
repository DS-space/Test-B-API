import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username, \
            f"Ожидаем, что username в запросе {login_user_request.username!r} соответсвует username в ответе {response.user.username!r}"
        assert response.user.role == "ROLE_ADMIN",\
            f"Ожидаем, что роль у админа 'ROLE_ADMIN', роль в ответе {response.user.role!r}"

    def test_login_user(self, api_manager: ApiManager, created_user_request: CreateUserRequest):
        response = api_manager.admin_steps.login_user(created_user_request)

        assert created_user_request.username == response.user.username, \
            f"Ожидаем, что username в запросе {created_user_request.username!r} соответсвует username в ответе {response.user.username!r}"
        assert response.user.role == "ROLE_USER", \
            f"Ожидаем, что роль у юзера 'ROLE_USER', роль в ответе {response.user.role!r}"