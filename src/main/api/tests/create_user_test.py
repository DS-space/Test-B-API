import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(
        self,
        api_manager: ApiManager,
        db_session: Session,
        create_user_request: CreateUserRequest,
    ):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username, \
            f"Ожидаем, что username в запросе {create_user_request.username!r} соответсвует username в ответе {response.user.username!r}"
        assert create_user_request.role == response.role, \
            f"Ожидаем, что роль в запросе {create_user_request.role!r} соответсвует роли в ответе {response.user.role!r} "

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.role == create_user_request.role, \
            f"Ожидаем, что роль пользователя в БД {user_from_db.role!r} соответсвует роли в запросе {create_user_request.role}, таблица User"

    @pytest.mark.parametrize(
        "username, password",
        [
            ("ккй", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("VMax1", "Pas!sw0rд"),
            ("VMax2", "Pas!sw0"),
            ("VMax3", "pas!sw0rd"),
            ("VMax4", "PASSW!0RD"),
            ("VMax5", "PASSW0RDdd"),
            ("VMax6", "PASSW!RDdd"),
        ]
    )
    def test_create_user_invalid(
        self,
        api_manager: ApiManager,
        db_session: Session,
        username: str,
        password: str,
    ):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, \
            f"Ожидаем, что пользователя {create_user_request.username!r} нет в БД, таблица User"




