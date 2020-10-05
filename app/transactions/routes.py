from typing import List

from fastapi import UploadFile, File, APIRouter, HTTPException
from starlette.responses import RedirectResponse

from .models import TransactionCollection, TransactionRecord, AcceptedContentTypes
from .operations import load_file, parse_and_process

router = APIRouter()


@router.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("/docs")


@router.post("/transactions/validate", response_model=TransactionCollection, tags=["JSON"])
def validate_transaction_collection(transactions: List[TransactionRecord]):
    """
    Validate a list of transactions in JSON format. Will automatically check if all reference ID's are unique
    """
    result = parse_and_process(transactions, AcceptedContentTypes.JSON)

    return result


@router.post("/transactions/validate/single", tags=["JSON"], response_model=TransactionCollection)
def validate_transaction_single(transaction: TransactionRecord):
    """
    Validate a single transaction.
    """
    result = parse_and_process([transaction], AcceptedContentTypes.JSON)

    return result


@router.post("/transactions/validate/upload",
             response_model=TransactionCollection,
             tags=["File"])
def validate_transactions_upload(
    file: UploadFile = File(...)
) -> TransactionCollection:
    """
    Validate a list of transactions from a file upload. Will validate reference uniqueness
    """
    try:
        content_type = AcceptedContentTypes(file.content_type)
    except Exception:
        raise HTTPException(status_code=400,
                            detail=f"Invalid content type {file.content_type}. Allowed content types are XML, CSV and JSON")

    try:
        file_rows = load_file(content_type, file.file)
    except Exception:
        raise HTTPException(status_code=400,
                            detail="Cannot deconde contents of the file")

    result = parse_and_process(file_rows, content_type)

    return result
