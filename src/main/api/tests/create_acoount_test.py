import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_with_account import UserWithAccount


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(
        self,
        api_manager: ApiManager,
        db_session: Session,
        created_user_request: CreateUserRequest,
    ):
        response = api_manager.user_steps.create_account(created_user_request)

        assert response.balance == 0

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, "Аккаунт не создан, id аккаунта нет в БД"
        assert account_from_db.balance is not None, "Поле баланса для созданного аккаунта отсутсвует в БД"

    def test_create_second_account(
        self,
        api_manager: ApiManager,
        db_session: Session,
        user_with_account: UserWithAccount,
    ):
        api_manager.user_steps.create_account(user_with_account.create_user_request)

        count_accounts_from_db = Account.count_accounts_by_user_id(db_session, user_with_account.user_id)
        assert count_accounts_from_db == 2, "Количество счетов не 2, ошибка"

    def test_create_account_invalid(
        self,
        api_manager: ApiManager,
        db_session: Session,
        user_with_two_accounts: UserWithAccount,
    ):
        api_manager.user_steps.create_account_invalid(user_with_two_accounts.create_user_request)

        count_accounts_from_db = Account.count_accounts_by_user_id(db_session, user_with_two_accounts.user_id)
        assert count_accounts_from_db == 2, "Изменилось количество счетов на аккаунте, ошибка"