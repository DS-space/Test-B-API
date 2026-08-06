import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestGetAllUsers:
    def test_get_all_users(
        self,
        api_manager: ApiManager,
        db_session: Session,
    ):
        response = api_manager.admin_steps.get_all_users()

        count_users_from_db = User.count_all_users(db_session)
        assert len(response.root) == count_users_from_db, "Количество пользователей в БД не соответсвует количеству в запросе, таблица User"