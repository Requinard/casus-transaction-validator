from decimal import Decimal
from typing import List, Union

from pydantic import BaseModel, Field, StrictInt, validator, ValidationError, root_validator
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
    def validate_transaction(self, start_balance: Decimal, end_balance: Decimal):
        if start_balance + self._get_mutation_amount() != end_balance:
            raise ValueError("This transaction does not add up!")

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
        if not isinstance(v, str):
            raise TypeError('string required')

        if v[0] not in ["+", "-"]:
            raise TypeError("First character of a mutation must be + or -")

        try:
            Decimal(v[1:])
        except:
            raise TypeError("All other characters must be parsable to a decimal")


class TransactionRecord(BaseModel):
    """
    Validate a single transaction
    """
    reference: StrictInt = Field(..., alias="Reference")
    account_number: str = Field(..., alias="Account Number")
    description: str = Field(..., alias="Description")
    start_balance: Decimal = Field(..., alias="Start Balance")
    mutation: Mutation = Field(..., alias="Mutation")  # todo test if this works out
    end_balance: Decimal = Field(..., alias="End Balance")

    @validator("account_number")
    def validate_account_number(cls, v):
        try:
            IBAN(v)
        except ValueError as e:
            raise ValidationError(e)


class FailedTransaction(BaseModel):
    transaction: TransactionRecord
    failures: List[Union[ValidationError, ValueError]]

    class Config:
        # Enable arbitrary types to show specific errors for the failures
        arbitrary_types_allowed = True


class TransactionCollection(BaseModel):
    """
    Validate a group of transactions
    """
    transactions: List[TransactionRecord]
    failed_transactions: List[FailedTransaction] = []

    @root_validator
    def validate_unique_references(cls, values):
        references = set()

        for item in values["transactions"]:
            if item.reference in references:
                failed_transaction = FailedTransaction(
                    transaction=item,
                    failures=[
                        ValueError("This unique reference was already listed!")
                    ]
                )
                values['failed_transactions'].append(failed_transaction)
            else:
                references.add(item.reference)
        return values
