from typing import Union

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_credit_request import CreateUserCreditRequest


class UserWithActiveCredit(BaseModel):
    create_user_request: CreateUserCreditRequest
    credit_id: int
    account_id: int
    amount: Union[float, int]