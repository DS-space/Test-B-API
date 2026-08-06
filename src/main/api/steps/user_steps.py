from requests import Response

from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validated_crud_requester import ValidateCrudRequester
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_apply_request import CreditApplyRequest
from src.main.api.models.credit_repayment_request import CreditRepaymentRequest
from src.main.api.models.deposit_account_invalid_request import DepositAccountInvalidRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(
        self,
        create_user_request: CreateUserRequest
    ) -> BaseModel:
        response = (
            ValidateCrudRequester(
                RequestSpecs.auth_headers(
                    username=create_user_request.username,
                    password=create_user_request.password
                ),
                Endpoint.CREATE_ACCOUNT,
                ResponseSpecs.request_created()
            ).post()
        )

        return response

    def create_account_invalid(
        self,
        create_user_request: CreateUserRequest
    ) -> None:
        CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREATE_ACCOUNT_INVALID,
            ResponseSpecs.request_conflict()
        ).post()

    def deposit_account(
        self,
        create_user_request: CreateUserRequest,
        deposit_account_request: DepositAccountRequest
    ) -> BaseModel:
        response = (
            ValidateCrudRequester(
                RequestSpecs.auth_headers(
                    username=create_user_request.username,
                    password=create_user_request.password
                ),
                Endpoint.USER_DEPOSIT,
                ResponseSpecs.request_ok()
            ).post(deposit_account_request)
        )

        return response

    def deposit_account_invalid(
        self,
        create_user_request: CreateUserRequest,
        deposit_account_request: DepositAccountInvalidRequest
    ) -> None:
        CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.USER_DEPOSIT_INVALID,
            ResponseSpecs.request_bad()
        ).post(deposit_account_request)

    def transfer(
        self,
        create_user_request: CreateUserRequest,
        transfer_request: TransferRequest
    ) -> BaseModel:
        response = (
            ValidateCrudRequester(
                RequestSpecs.auth_headers(
                    username=create_user_request.username,
                    password=create_user_request.password
                ),
                Endpoint.TRANSFER,
                ResponseSpecs.request_ok()
            ).post(transfer_request)
        )

        return response

    def transfer_invalid(
            self,
            create_user_request: CreateUserRequest,
            transfer_request: TransferRequest
    ) -> Response:
        response = (
            CrudRequester(
                RequestSpecs.auth_headers(
                    username=create_user_request.username,
                    password=create_user_request.password
                ),
                Endpoint.TRANSFER_INVALID,
                ResponseSpecs.request_bad()
            ).post(transfer_request)
        )

        return response

    def credit_apply(
            self,
            create_user_request: CreateUserRequest,
            credit_apply_request: CreditApplyRequest
    ) -> BaseModel:
        response = (
            ValidateCrudRequester(
                RequestSpecs.auth_headers(
                    username=create_user_request.username,
                    password=create_user_request.password
                ),
                Endpoint.CREDIT_APPLY,
                ResponseSpecs.request_created()
            ).post(credit_apply_request)
        )

        return response

    def credit_apply_invalid(
        self,
        create_user_request: CreateUserRequest,
        credit_apply_request: CreditApplyRequest
    ) -> Response:
        response = (
            CrudRequester(
                RequestSpecs.auth_headers(
                    username=create_user_request.username,
                    password=create_user_request.password
                ),
                Endpoint.CREDIT_APPLY_INVALID,
                ResponseSpecs.request_bad()
            ).post(credit_apply_request)
        )

        return response

    def repayment(
        self,
        create_user_request: CreateUserRequest,
        credit_repayment_request: CreditRepaymentRequest
    ) -> BaseModel:
        response = (
            ValidateCrudRequester(
                RequestSpecs.auth_headers(
                    username=create_user_request.username,
                    password=create_user_request.password
                ),
                Endpoint.CREDIT_REPAYMENT,
                ResponseSpecs.request_ok()
            ).post(credit_repayment_request)
        )

        return response

    def repayment_invalid(
        self,
        create_user_request: CreateUserRequest,
        credit_repayment_request: CreditRepaymentRequest
    ) -> Response:
        response = (
            CrudRequester(
                RequestSpecs.auth_headers(
                    username=create_user_request.username,
                    password=create_user_request.password
                ),
                Endpoint.CREDIT_REPAYMENT,
                ResponseSpecs.request_unprocessable_entity()
            ).post(credit_repayment_request)
        )

        return response