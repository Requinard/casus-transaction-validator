from typing import List, Union

from pydantic import BaseModel, Field, StrictInt, validator, ValidationError, root_validator
from schwifty import IBAN


class TransactionRecord(BaseModel):
    """
    Validate a single transaction
    """
    reference: StrictInt = Field(..., alias="Reference")
    account_number: str = Field(..., alias="Account Number")
    description: str = Field(..., alias="Description")
    start_balance: str = Field(..., alias="Start Balance")
    mutation: str = Field(..., alias="Mutation")
    end_balance: str = Field(..., alias="End Balance")

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
