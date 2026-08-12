from pydantic import RootModel

from src.main.api.models.base_model import BaseModel


class User(BaseModel):
    id: int
    username: str
    role: str


class GetAllUsersResponse(RootModel[list[User]]):
    pass