from typing import Union

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_request import CreateUserRequest


class UserWithTwoDeposits(BaseModel):
    user_request: CreateUserRequest
    account_id: int
    balance: Union[float, int]