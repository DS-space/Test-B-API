from src.main.api.models.base_model import BaseModel


class CreditRepaymentResponse(BaseModel):
    creditId: int
    amountDeposited: float