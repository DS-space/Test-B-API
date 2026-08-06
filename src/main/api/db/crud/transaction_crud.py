from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(id=transaction_id).first()

    @staticmethod
    def get_transaction_by_account_id(db: Session, account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=account_id).first()

    @staticmethod
    def get_transaction_transfer_by_accounts_id(
        db: Session,
        owner_account_id: int,
        recipient_account_id: int
    ) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=owner_account_id, to_account_id=recipient_account_id).first()

    @staticmethod
    def get_transaction_by_credit_id(
            db: Session,
            credit_id: int
    ) -> Transaction | None:
        return db.query(Transaction).filter_by(credit_id=credit_id).first()