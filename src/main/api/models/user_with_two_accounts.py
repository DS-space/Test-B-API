from typing import Union

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_request import CreateUserRequest


class UserWithTwoAccounts(BaseModel):
    create_user_request: CreateUserRequest
    user_id: int
    first_account_id: int
    first_balance: Union[float, int]
    second_account_id: int
    second_balance: Union[float, int]