from sqlalchemy import Integer, Float, DateTime, Column, ForeignKey

from src.main.api.db.base import Base


class Credit(Base):
    __tablename__ = "credit"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    amount = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    balance = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return (
            f"<Credit("
            f"{self.id!r}, {self.account_id!r}, "
            f"{self.amount!r}, {self.term_months!r}"
            f"{self.balance!r}, "
            f"{self.created_at})>"
        )


