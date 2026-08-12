from typing import Optional

from src.main.api.models.base_model import BaseModel


class TransactionItem(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int] = None
    toAccountId: int
    createdAt: str
    creditId: Optional[int] = None


class TransactionsHistoryResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: list[TransactionItem]