from src.main.api.models.base_model import BaseModel


class Credit(BaseModel):
    creditId: int
    accountId: int
    amount: float
    termMonths: int
    balance: float
    createdAt: str


class UserCreditHistoryResponse(BaseModel):
    userId: int
    credits: list[Credit]
