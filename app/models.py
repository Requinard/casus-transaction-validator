from decimal import Decimal
from typing import List, Any, Tuple, Union, Callable

from pydantic import BaseModel, Field, validator, ValidationError, PositiveInt
from schwifty import IBAN


class Mutation(str):
    def _get_sign(self):
        """
        Gets the sign
        """

        if str(self)[0] == "-":
            return Decimal(-1)
        elif str(self)[0] == "+":
            return Decimal(1)

        raise ValueError("Unknown sign in mutation")

    def _get_number(self):
        return Decimal(str(self)[1:])

    def _get_mutation_amount(self):
        return self._get_sign() * self._get_number()

    # todo validate mutation
    def validate_transaction(self, start_balance: Decimal, end_balance: Decimal, reference: PositiveInt):
        if start_balance + self._get_mutation_amount() != end_balance:
            raise ValueError(f"Transaction {reference} does not add up")

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            examples=['-1.0', '+1.0', '-1.20'],
        )

    @classmethod
    def validate(cls, v):
        if v[0] not in ["+", "-"]:
            raise TypeError("First character of a mutation must be + or -")

        try:
            Decimal(v[1:])
        except:
            raise TypeError("All other characters must be parsable to a decimal")

    class Config:
        allow_population_by_field_name = True


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


ErrorType = Union[ValidationError, Any]
FailedTransaction = Tuple[Any, str]
TransactionTypes = Union[TransactionRecord, XMLTransactionRecord, CSVTransactionRecord]


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
