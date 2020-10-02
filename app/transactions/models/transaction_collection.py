from typing import List, Any, Callable

from pydantic.main import BaseModel

from .transaction_record import FailedTransaction, TransactionTypes, CSVTransactionRecord, XMLTransactionRecord, \
    TransactionRecord


class TransactionCollection(BaseModel):
    """
    Validate a group of transactions
    """
    content_type: str
    raw_transactions: List[Any]
    invalid_transactions: List[FailedTransaction] = []
    valid_transactions: List[TransactionTypes] = []

    def get_validator(self):
        if self.content_type == 'text/csv':
            return CSVTransactionRecord.validate
        elif self.content_type == 'text/xml':
            return XMLTransactionRecord.validate
        else:
            return TransactionRecord.validate

    def process(self):
        """
        Process all raw transactions and sort them into valid or invalid categories
        """
        existing_references = set()
        validator: Callable = self.get_validator()

        for item in self.raw_transactions:
            try:
                transaction: TransactionRecord = validator(item)
                transaction.check_amount_validity()

                if transaction.reference in existing_references:
                    raise ValueError(f"Transaction {transaction.reference} already exists!")

                existing_references.add(transaction.reference)
                self.valid_transactions.append(transaction)
            except Exception as e:
                self.invalid_transactions.append(
                    tuple([item, str(e)]))  # todo: this does not show up as it should. Error is empty

    class Config:
        # Enable arbitrary types to show specific errors for the failures
        arbitrary_types_allowed = True
