from typing import List

from pydantic import BaseModel, Field
from pydantic.types import Decimal


class TransactionRecord(BaseModel):
    """
    Validate a single transaction
    """
    reference: Decimal = Field(..., alias="Reference")
    account_number: str = Field(..., alias="Account Number")
    description: str = Field(..., alias="Description")
    start_balance: str = Field(..., alias="Start Balance")
    mutation: str = Field(..., alias="Mutation")
    end_balance: str = Field(..., alias="End Balance")


class TransactionGroup(BaseModel):
    """
    Validate a group of transactions
    """
    transactions: List[TransactionRecord] = []
