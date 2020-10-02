from decimal import Decimal
from typing import Tuple, Any, Union

from pydantic import PositiveInt, BaseModel, Field, ValidationError, validator
from schwifty import IBAN

from .mutation import Mutation


class TransactionRecord(BaseModel):
    """
    Validate a single transaction
    """
    reference: PositiveInt = Field(...)
    account_number: str = Field(...)
    description: str = Field(...)
    start_balance: Decimal = Field(...)
    mutation: str = Field(...)
    end_balance: Decimal = Field(...)

    def check_amount_validity(self):
        m = Mutation(self.mutation)

        m.validate_transaction(self.start_balance, self.end_balance, self.reference)

    @validator('mutation')
    def validate_mutation_format(cls, v):
        Mutation(v)

        return v

    @validator("account_number")
    def validate_account_number(cls, v):
        try:
            IBAN(v)
        except ValueError as e:
            raise ValidationError(e)

        return v


class CSVTransactionRecord(TransactionRecord):
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
    class Config:
        fields = {
            'reference': 'reference',
            'account_number': 'accountNumber',
            'description': 'description',
            'start_balance': 'startBalance',
            'mutation': 'mutation',
            'end_balance': 'endBalance'
        }


FailedTransaction = Tuple[Any, str]
TransactionTypes = Union[TransactionRecord, XMLTransactionRecord, CSVTransactionRecord]
