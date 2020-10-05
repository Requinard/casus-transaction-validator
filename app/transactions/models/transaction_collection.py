import mimetypes
from enum import Enum
from os import PathLike
from typing import List, Any, Callable

from pydantic.main import BaseModel

from .transaction_record import FailedTransaction, TransactionTypes, CSVTransactionRecord, XMLTransactionRecord, \
    TransactionRecord


class AcceptedContentTypes(str, Enum):
    CSV = "text/csv"
    XML = "text/xml"
    JSON = "application/json"

    @staticmethod
    def guess(f: PathLike):
        mimetype = mimetypes.guess_type(f)
        return AcceptedContentTypes(mimetype[0])


class TransactionCollection(BaseModel):
    """
    Validate a group of transactions.
    """
    content_type: AcceptedContentTypes
    raw_transactions: List[Any]
    invalid_transactions: List[FailedTransaction] = []
    valid_transactions: List[TransactionTypes] = []

    def get_validator(self) -> Callable:
        """
        Get a validator based on our internal content_type. XML, CSV and JSON all have their own names and thus need their
        own validation model.

        :return: A validation function that returns a validated object, or throws a ValidationError
        """
        if self.content_type == AcceptedContentTypes.CSV:
            return CSVTransactionRecord.validate
        elif self.content_type == AcceptedContentTypes.XML:
            return XMLTransactionRecord.validate
        else:
            return TransactionRecord.validate

    def process(self):
        """
        Process all raw transactions and sort them into valid or invalid categories.

        First, transactions are loaded as raw, untyped objects.
        Then we call the validator function to see if they fit into our idea of a valid transaction
        Then we check if we have already seen this transaction ID
        If any errors occur in this stage, add it to invalid transactions, along with the error message
        If no errors occur, we add the fully typed transaction to valid_transactions
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
                self.invalid_transactions.append((item, str(e)))

    class Config:
        # Enable arbitrary types to show specific errors for the failures
        arbitrary_types_allowed = True
