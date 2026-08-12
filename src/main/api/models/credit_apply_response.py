from src.main.api.models.base_model import BaseModel


class CreditApplyResponse(BaseModel):
    id: int
    amount: float
    termMonths: int
    balance: float
    creditId: int
