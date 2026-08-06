from typing import Union

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.transaction_table import Transaction
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.models.user_with_two_deposits import UserWithTwoDeposits


@pytest.mark.api
class TestTransfer:
    @pytest.mark.parametrize(
        "amount",
        [500, 500.01, 9999.99, 10000]
    )
    def test_transfer_to_another_user(
        self,
        api_manager: ApiManager,
        db_session: Session,
        user_with_two_9k_deposits: UserWithTwoDeposits,
        recipient_account: CreateAccountResponse,
        amount: Union[int, float],
    ):
        transfer_request = TransferRequest(
            fromAccountId=user_with_two_9k_deposits.account_id,
            toAccountId=recipient_account.id,
            amount=amount
        )
        response = api_manager.user_steps.transfer(
            user_with_two_9k_deposits.user_request,
            transfer_request
        )

        assert response.fromAccountIdBalance == user_with_two_9k_deposits.balance - amount

        owner_account_from_db = Account.get_account_by_id(db_session, user_with_two_9k_deposits.account_id)
        assert owner_account_from_db.balance == user_with_two_9k_deposits.balance - amount, "Баланс в БД не соответсвует ожидаемому (Баланс до перевода - сумма перевода), таблица Account"

        recipient_account_from_db = Account.get_account_by_id(db_session, recipient_account.id)
        assert recipient_account_from_db.balance == amount, "Баланс в БД не соответсвует ожидаемому, таблица Account"

        transaction_from_db = Transaction.get_transaction_transfer_by_accounts_id(db_session, user_with_two_9k_deposits.account_id, recipient_account.id)
        assert transaction_from_db.amount == amount, "Сумма перевода в БД не соответсвует сумме перевода в запросе, таблица Transaction"

    @pytest.mark.parametrize(
        "amount",
        [-1, 0, 499.99, 15000.01]
    )
    def test_transfer_to_another_user_invalid(
        self,
        api_manager: ApiManager,
        db_session: Session,
        user_with_two_9k_deposits: UserWithTwoDeposits,
        recipient_account: CreateAccountResponse,
        amount: Union[float, int],
    ):
        transfer_request = TransferRequest(
            fromAccountId=user_with_two_9k_deposits.account_id,
            toAccountId=recipient_account.id,
            amount=amount
        )

        api_manager.user_steps.transfer_invalid(
            user_with_two_9k_deposits.user_request,
            transfer_request
        )

        owner_account_from_db = Account.get_account_by_id(db_session, user_with_two_9k_deposits.account_id)
        assert owner_account_from_db.balance == user_with_two_9k_deposits.balance, "Изменился баланс в БД у отправителя, таблица Account"

        recipient_account_from_db = Account.get_account_by_id(db_session, recipient_account.id)
        assert recipient_account_from_db.balance == 0, "Баланс у получателя не 0, таблица Account"

        transaction_from_db = Transaction.get_transaction_transfer_by_accounts_id(db_session, user_with_two_9k_deposits.account_id, recipient_account.id)
        assert transaction_from_db is None, "Транзакция есть в БД, ошибка, таблица Transaction"










