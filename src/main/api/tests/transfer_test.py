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
from src.main.api.models.user_with_account import UserWithAccount
from src.main.api.models.user_with_two_deposits import UserWithTwoDeposits
from src.main.api.models.user_with_two_accounts import UserWithTwoAccounts


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

        assert response.fromAccountIdBalance == user_with_two_9k_deposits.balance - amount, \
            (f"Ожидаем, что баланс отправителя в ответе {response.fromAccountIdBalance} соответсвует "
             f"сумме(баланс до перевода - сумма перевода) {user_with_two_9k_deposits.balance - amount}")

        owner_account_from_db = Account.get_account_by_id(db_session, user_with_two_9k_deposits.account_id)
        assert owner_account_from_db.balance == user_with_two_9k_deposits.balance - amount, \
            (f"Ожидаем, что баланс отправителя в БД {owner_account_from_db.balance} соответсвует "
             f"сумме(баланс до перевода - сумма перевода) {user_with_two_9k_deposits.balance - amount}, таблица Account")

        recipient_account_from_db = Account.get_account_by_id(db_session, recipient_account.id)
        assert recipient_account_from_db.balance == amount, \
            f"Ожидаем, что баланс получателя в БД {recipient_account_from_db.balance} соответсвует сумме перевода {amount}, таблица Account"

        transaction_from_db = Transaction.get_transaction_transfer_by_accounts_id(db_session, user_with_two_9k_deposits.account_id, recipient_account.id)
        assert transaction_from_db.amount == amount, \
            f"Ожидаем, что сумма транзакции в БД {transaction_from_db.amount} соответсвует сумме перевода {amount}, таблица Transaction"

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
        assert owner_account_from_db.balance == user_with_two_9k_deposits.balance, \
            (f"Ожидаем, что баланс отправителся в БД {owner_account_from_db.balance} не изменился и "
             f"равен балансу в ответе депозита{user_with_two_9k_deposits.balance}, таблица Account")

        recipient_account_from_db = Account.get_account_by_id(db_session, recipient_account.id)
        assert recipient_account_from_db.balance == 0, \
            f"Ожидаем, что баланс получателя в БД {recipient_account_from_db.balance} не изменился и равен нулю, таблица Account"

        transaction_from_db = Transaction.get_transaction_transfer_by_accounts_id(db_session, user_with_two_9k_deposits.account_id, recipient_account.id)
        assert transaction_from_db is None, \
            f"Ожидаем, что транзакции в БД по этому счёту нет, транзакция: {transaction_from_db}, таблица Transaction"

    def test_transfer_to_self(
        self,
        api_manager: ApiManager,
        db_session: Session,
        user_with_two_accounts: UserWithTwoAccounts
    ):
        transfer_request = TransferRequest(
            fromAccountId=user_with_two_accounts.first_account_id,
            toAccountId=user_with_two_accounts.second_account_id,
            amount=user_with_two_accounts.first_balance
        )

        response = api_manager.user_steps.transfer(
            user_with_two_accounts.create_user_request,
            transfer_request
        )

        assert response.fromAccountIdBalance == 0, \
            f"Ожидаем, что баланс счёта равен 0, баланс в ответе: {response.fromAccountIdBalance}"

        sender_account_from_db = Account.get_account_by_id(db_session, user_with_two_accounts.first_account_id)
        assert sender_account_from_db.balance == 0, \
            f"Ожидаем, что баланс счёта в БД равен 0, баланс в БД: {sender_account_from_db.balance}"

        recipient_account_from_db = Account.get_account_by_id(db_session, user_with_two_accounts.second_account_id)
        assert recipient_account_from_db.balance == user_with_two_accounts.second_balance + user_with_two_accounts.first_balance, \
            f"Ожидаем, что баланс счёта на который переводим"








