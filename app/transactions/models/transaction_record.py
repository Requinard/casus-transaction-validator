from decimal import Decimal
from typing import Tuple, Any, Union

from pydantic import PositiveInt, BaseModel, Field, ValidationError, validator
from schwifty import IBAN

from .mutation import Mutation


class TransactionRecord(BaseModel):
    """
    Model that holds all rules to validate a single transaction.
    """
    reference: PositiveInt = Field(..., description="A unique reference positive integer for this transaction")
    account_number: str = Field(..., description="A valid IBAN account string")
    description: str = Field(..., description="A description of the transaction")
    start_balance: Decimal = Field(...)
    mutation: Mutation = Field(...)
    end_balance: Decimal = Field(...)

    def check_amount_validity(self):
        m = Mutation(self.mutation)

        m.validate_transaction(self.start_balance, self.end_balance, self.reference)

    @validator("account_number")
    def validate_account_number(cls, v):
        """
        Check if the account number is a valid IBAN
        """
        try:
            IBAN(v)
        except ValueError as e:
            raise ValidationError(e)

        return v


class CSVTransactionRecord(TransactionRecord):
    """
    A sub-class of TransactionRecord that allows us to read CSV-specific field names into our generic model.
    """

    class Config:
        fields = {
            'reference': 'Reference',
            'account_number': 'Account Number',
            'description': 'Description',
            'start_balance': 'Start Balance',
            'mutation': 'Mutation',
            'end_balance': 'End Balance'
        }


class XMLTransactionRecord(TransactionRecord):
    """
    A sub-class of TransactionRecord that allows us to read XML-specific field names into our generic model
    """

    class Config:
        fields = {
            'reference': 'reference',
            'account_number': 'accountNumber',
            'description': 'description',
            'start_balance': 'startBalance',
            'mutation': 'mutation',
            'end_balance': 'endBalance'
        }


# Describe a failed transaction
FailedTransaction = Tuple[Any, str]

# Compound all possible transaction types into a single type
TransactionTypes = Union[TransactionRecord, XMLTransactionRecord, CSVTransactionRecord]
