from src.main.api.models.base_model import BaseModel


class CreditRepaymentRequest(BaseModel):
    creditId: int
    accountId: int
    amount: float