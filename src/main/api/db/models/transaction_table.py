from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey

from src.main.api.db.base import Base


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    to_account_id = Column(Integer, ForeignKey("account.id"))
    from_account_id = Column(Integer, ForeignKey("account.id"))
    credit_id = Column(Integer, ForeignKey("credit.id"))
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return (
            f"<Transaction("
            f"{self.id!r}, {self.to_account_id!r}, "
            f"{self.from_account_id!r}, {self.credit_id!r}, "
            f"{self.amount!r}, {self.transaction_type!r}, "
            f"{self.created_at!r}"
            f")>"
        )
