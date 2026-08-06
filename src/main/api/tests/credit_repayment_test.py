import pytest
from sqlalchemy.orm import Session

from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.transaction_table import Transaction
from src.main.api.models.credit_repayment_request import CreditRepaymentRequest
from src.main.api.models.user_with_active_credit import UserWithActiveCredit
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestCreditRepayment:
    def test_repayment(
        self,
        api_manager: ApiManager,
        db_session: Session,
        credit_role_user_with_loan: UserWithActiveCredit
    ):
        repayment_request = CreditRepaymentRequest(
            creditId=credit_role_user_with_loan.credit_id,
            accountId=credit_role_user_with_loan.account_id,
            amount=credit_role_user_with_loan.amount
        )
        response = api_manager.user_steps.repayment(credit_role_user_with_loan.create_user_request, repayment_request)

        assert response.amountDeposited == repayment_request.amount
        assert response.creditId == repayment_request.creditId

        credit_info_from_db = Credit.get_credit_by_id(
            db_session,
            credit_role_user_with_loan.credit_id
        )
        assert credit_info_from_db.balance == 0, "Баланс в БД не 0, таблица Credit"

        transaction_from_db = Transaction.get_transaction_by_credit_id(
            db_session,
            credit_role_user_with_loan.credit_id
        )
        assert transaction_from_db.amount == credit_role_user_with_loan.amount, "Сумма транзакции в БД не соответсвует сумме в запросе, таблица Transaction"


    def test_repayment_invalid(
        self,
        api_manager: ApiManager,
        db_session: Session,
        credit_role_user_with_loan: UserWithActiveCredit
    ):
        repayment_request = CreditRepaymentRequest(
            creditId=credit_role_user_with_loan.credit_id,
            accountId=credit_role_user_with_loan.account_id,
            amount=credit_role_user_with_loan.amount - 0.01
        )
        api_manager.user_steps.repayment_invalid(credit_role_user_with_loan.create_user_request, repayment_request)

        credit_info_from_db = Credit.get_credit_by_id(
            db_session,
            credit_role_user_with_loan.credit_id
        )
        assert credit_info_from_db.balance == -credit_role_user_with_loan.amount, "Баланс в БД не соответсвует задолжности юзера, таблица Credit"

        transaction_from_db = Transaction.get_transaction_by_credit_id(
            db_session, credit_role_user_with_loan.credit_id
        )
        assert transaction_from_db is None, "БД вернула запись транзакции, ожидали что транзакции в БД нет"


