import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_credit_request import CreateUserCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_apply_request import CreditApplyRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.user_credit_with_account import UserCreditWithAccount
from src.main.api.models.user_with_account import UserWithAccount
from src.main.api.models.user_with_active_credit import UserWithActiveCredit
from src.main.api.models.user_with_two_deposits import UserWithTwoDeposits


@pytest.fixture
def created_user_request(api_manager: ApiManager) -> BaseModel:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def created_account(
    api_manager: ApiManager,
    created_user_request: CreateUserRequest
) -> BaseModel:
    create_account_response = api_manager.user_steps.create_account(created_user_request)
    return create_account_response

@pytest.fixture
def user_with_two_9k_deposits(
    api_manager: ApiManager,
    created_user_request: CreateUserRequest,
    created_account: CreateAccountResponse
) -> BaseModel:
    max_amount = 9000

    api_manager.user_steps.deposit_account(
        created_user_request,
        DepositAccountRequest(
            accountId=created_account.id,
            amount=max_amount
        )
    )

    response = api_manager.user_steps.deposit_account(
        created_user_request,
        DepositAccountRequest(
            accountId=created_account.id,
            amount=max_amount
        )
    )

    return (
        UserWithTwoDeposits(
            user_request=created_user_request,
            account_id=response.id,
            balance=response.balance
            )
    )

@pytest.fixture
def recipient_account(api_manager: ApiManager) -> BaseModel:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    response = api_manager.user_steps.create_account(user_request)
    return response

@pytest.fixture
def user_with_account(api_manager: ApiManager) -> BaseModel:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_response = api_manager.admin_steps.create_user(user_request)
    api_manager.user_steps.create_account(user_request)
    return (
        UserWithAccount(
            create_user_request=user_request,
            user_id=user_response.id
        )
    )

@pytest.fixture
def user_with_two_accounts(api_manager: ApiManager) -> BaseModel:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_response = api_manager.admin_steps.create_user(user_request)
    api_manager.user_steps.create_account(user_request)
    api_manager.user_steps.create_account(user_request)
    return (
        UserWithAccount(
            create_user_request=user_request,
            user_id=user_response.id
        )
    )

@pytest.fixture
def created_user_credit_request(api_manager: ApiManager) -> BaseModel:
    user_request = RandomModelGenerator.generate(CreateUserCreditRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def credit_role_user_with_account(
    api_manager: ApiManager,
    created_user_credit_request: CreateUserCreditRequest
) -> BaseModel:
    response = api_manager.user_steps.create_account(created_user_credit_request)

    return (
        UserCreditWithAccount(
            create_user_request=created_user_credit_request,
            account_id=response.id,
            balance=response.balance
        )
    )

@pytest.fixture
def credit_role_user_with_loan(
    api_manager: ApiManager,
    credit_role_user_with_account: UserCreditWithAccount
) -> BaseModel:
    credit_apply_request = CreditApplyRequest(
        accountId=credit_role_user_with_account.account_id,
        amount=5000,
        termMonths=6
    )
    response = api_manager.user_steps.credit_apply(
        credit_role_user_with_account.create_user_request,
        credit_apply_request
    )

    return (
        UserWithActiveCredit(
            create_user_request=credit_role_user_with_account.create_user_request,
            credit_id=response.creditId,
            account_id=response.id,
            amount=response.amount
        )
    )