from typing import List

from fastapi import UploadFile, File, APIRouter
from starlette.responses import RedirectResponse

from .models import TransactionCollection, TransactionRecord, AcceptedContentTypes
from .operations import load_file, parse_to_models

router = APIRouter()


@router.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("/docs")


@router.post("/transactions/validate", response_model=TransactionCollection, tags=["JSON"])
def validate_transaction_collection(transactions: List[TransactionRecord]):
    """
    Validate a list of transactions in JSON format. Will automatically check if all reference ID's are unique
    """
    result = parse_to_models(transactions, "application/json")

    return result


@router.post("/transactions/validate/single", tags=["JSON"], response_model=TransactionCollection)
def validate_transaction_single(transaction: TransactionRecord):
    """
    Validate a single transaction.
    """
    result = parse_to_models([transaction], "application/json")

    return result


@router.post("/transactions/validate/upload", response_model=TransactionCollection, tags=["File"])
def validate_transactions_upload(
    file: UploadFile = File(...)
) -> TransactionCollection:
    """
    Validate a list of transactions from a file upload. Will validate reference uniqueness
    """
    if file.content_type not in list(AcceptedContentTypes):
        raise ValueError("File is not in an accepted content-type")

    file_rows = load_file(file)

    result = parse_to_models(file_rows, file.content_type)

    return result