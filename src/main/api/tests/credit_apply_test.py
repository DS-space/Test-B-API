from typing import Union

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.credit_apply_request import CreditApplyRequest
from src.main.api.models.user_credit_with_account import UserCreditWithAccount
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestCreditApply:
    @pytest.mark.parametrize(
        "amount, term_months",
        [
            (5000, 6),
            (5000.01, 12),
            (14999.99, 18),
            (15000, 24),
        ]
    )
    def test_credit_apply(
        self,
        api_manager: ApiManager,
        db_session: Session,
        credit_role_user_with_account: UserCreditWithAccount,
        amount: Union[float, int],
        term_months: int,
    ):
        credit_apply_request = CreditApplyRequest(
            accountId=credit_role_user_with_account.account_id,
            amount=amount,
            termMonths=term_months
        )
        response = api_manager.user_steps.credit_apply(
            credit_role_user_with_account.create_user_request,
            credit_apply_request
        )

        assert response.balance == credit_apply_request.amount, \
            f"Ожидаем, что баланс в ответе {response.balance} соответсвует сумме в запросе {credit_apply_request.amount}"
        assert response.termMonths == credit_apply_request.termMonths, \
            f"Ожидаем, что количество месяцев в ответе {response.termMonths} соответсвует количеству в запросе {credit_apply_request.termMonths}"

        account_from_db = Account.get_account_by_id(
            db_session,
            credit_role_user_with_account.account_id
        )
        assert account_from_db.balance == amount, \
            f"Ожидаем, что баланс в БД {account_from_db.balance} соответсвует сумме в запросе {amount}, таблица Account"

        credit_info_from_db = Credit.get_credit_by_account_id(
            db_session,
            credit_role_user_with_account.account_id
        )
        assert credit_info_from_db.amount == amount, \
            f"Ожидаем, что сумма кредита в БД {credit_info_from_db.amount} соответсвует сумме в запросе {amount}, таблица Credit"

        transaction_from_db = Transaction.get_transaction_by_account_id(
            db_session,
            credit_role_user_with_account.account_id
        )
        assert transaction_from_db.amount == amount, \
            f"Ожидаем, что сумма транзакции в БД {transaction_from_db.amount} соответсвует сумме кредита в запросе, таблица Transaction"

    @pytest.mark.parametrize(
        "amount, term_months",
        [
            (4999.99, 6),
            (15000.01, 6),
            (15001, 6),
            (7500, -6),
        ]
    )
    def test_credit_apply_invalid(
        self,
        api_manager: ApiManager,
        db_session: Session,
        credit_role_user_with_account: UserCreditWithAccount,
        amount: Union[float, int],
        term_months: int,
    ):
        credit_apply_request = CreditApplyRequest(
            accountId=credit_role_user_with_account.account_id,
            amount=amount,
            termMonths=term_months
        )
        api_manager.user_steps.credit_apply_invalid(
            credit_role_user_with_account.create_user_request,
            credit_apply_request
        )

        account_from_db = Account.get_account_by_id(
            db_session,
            credit_role_user_with_account.account_id
        )
        assert account_from_db.balance == 0, \
            f"Ожидаем, что баланс в БД не изменился и равен 0, баланс в БД: {account_from_db.balance}, таблица Account"

        credit_info_from_db = Credit.get_credit_by_account_id(
            db_session,
            credit_role_user_with_account.account_id
        )
        assert credit_info_from_db is None, \
            f"Ожидаем, что у аккаунта нет кредита в БД, запись: {credit_info_from_db}, таблица Credit"

        transaction_from_db = Transaction.get_transaction_by_account_id(
            db_session,
            credit_role_user_with_account.account_id
        )
        assert transaction_from_db is None, \
            f"Ожидаем, что у аккаунта нет транзакций в БД, транзакция: {transaction_from_db}, таблица Transaction"










