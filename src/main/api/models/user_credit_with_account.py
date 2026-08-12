from typing import Union

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_credit_request import CreateUserCreditRequest


class UserCreditWithAccount(BaseModel):
    create_user_request: CreateUserCreditRequest
    account_id: int
    balance: Union[float, int]