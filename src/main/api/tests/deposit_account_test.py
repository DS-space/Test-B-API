from typing import Union

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_invalid_request import DepositAccountInvalidRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize(
        "amount",
        [1000, 1000.01, 8999.99, 9000]
    )
    def test_deposit(
        self,
        api_manager: ApiManager,
        db_session: Session,
        created_user_request: CreateUserRequest,
        created_account: CreateAccountResponse,
        amount: Union[float, int],
    ):
        deposit_account_request = DepositAccountRequest(accountId=created_account.id, amount=amount)
        response = api_manager.user_steps.deposit_account(created_user_request, deposit_account_request)

        assert response.balance == deposit_account_request.amount

        account_from_db = Account.get_account_by_id(db_session, created_account.id)
        assert account_from_db.balance == response.balance, "Баланс в ответе не соответствует балансу в БД, таблица Account"

        deposit_transaction_from_db = Transaction.get_transaction_by_account_id(db_session, response.id)
        assert deposit_transaction_from_db.amount == deposit_account_request.amount, "Сумма в БД не соответсвует сумме в запросе, таблица Transaction"

    @pytest.mark.parametrize(
        "amount",
        [999, 999.99, 9000.01, 9001]
    )
    def test_deposit_invalid(
        self,
        api_manager: ApiManager,
        db_session: Session,
        created_user_request: CreateUserRequest,
        created_account: CreateAccountResponse,
        amount: Union[float, int],
    ):
        deposit_account_request = DepositAccountInvalidRequest(
                accountId=created_account.id,
                amount=amount
            )
        api_manager.user_steps.deposit_account_invalid(
            created_user_request,
            deposit_account_request
        )

        deposits_account_from_db = Transaction.get_transaction_by_account_id(db_session, created_account.id)
        assert deposits_account_from_db is None, "По счёту найдены транзакции, ошибка"

        account_from_db = Account.get_account_by_id(db_session, created_account.id)
        assert account_from_db.balance == 0, "Баланс счёта должен быть нулевым, ошибка"

