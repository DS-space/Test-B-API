from sqlalchemy import Column, Integer, String, Float, ForeignKey

from src.main.api.db.base import Base


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    number = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Account({self.id!r}, {self.user_id!r}, {self.number!r}, {self.balance!r})>"