from enum import Enum
from typing import Optional, Type
from dataclasses import dataclass

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_apply_request import CreditApplyRequest
from src.main.api.models.credit_apply_response import CreditApplyResponse
from src.main.api.models.credit_repayment_request import CreditRepaymentRequest
from src.main.api.models.credit_repayment_response import CreditRepaymentResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.deposit_account_invalid_request import DepositAccountInvalidRequest
from src.main.api.models.get_all_users_response import GetAllUsersResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model = CreateUserRequest,
        url = "/admin/create",
        response_model = CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model = None,
        url = "/admin/users",
        response_model = None
    )

    ADMIN_GET_ALL_USERS = EndpointConfiguration(
        request_model = None,
        url = "/admin/users",
        response_model = GetAllUsersResponse
    )

    LOGIN_USER = EndpointConfiguration(
        request_model = LoginUserRequest,
        url = "/auth/token/login",
        response_model = LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model = None,
        url = "/account/create",
        response_model= CreateAccountResponse
    )

    CREATE_ACCOUNT_INVALID = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=None
    )

    USER_DEPOSIT = EndpointConfiguration(
        request_model = DepositAccountRequest,
        url = "/account/deposit",
        response_model = DepositAccountResponse
    )

    USER_DEPOSIT_INVALID = EndpointConfiguration(
        request_model = DepositAccountInvalidRequest,
        url = "/account/deposit",
        response_model = None
    )

    TRANSFER = EndpointConfiguration(
        request_model = TransferRequest,
        url = "/account/transfer",
        response_model = TransferResponse
    )

    TRANSFER_INVALID = EndpointConfiguration(
        request_model = TransferRequest,
        url = "/account/transfer",
        response_model = None
    )

    CREDIT_APPLY = EndpointConfiguration(
        request_model = CreditApplyRequest,
        url = "/credit/request",
        response_model = CreditApplyResponse
    )

    CREDIT_APPLY_INVALID = EndpointConfiguration(
        request_model = CreditApplyRequest,
        url = "/credit/request",
        response_model = None
    )

    CREDIT_REPAYMENT = EndpointConfiguration(
        request_model=CreditRepaymentRequest,
        url="/credit/repay",
        response_model = CreditRepaymentResponse
    )