from fastapi import FastAPI, UploadFile, File
from starlette.responses import RedirectResponse

from models import TransactionCollection
from operations import load_file

app = FastAPI(
    title="ACME Transaction Validator"
)

accepted_content_types = [
    "text/xml",
    "text/csv"
]


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("/docs")


@app.post("/validate_transactions")
def validate_transactions(
        file: UploadFile = File(...)
) -> TransactionCollection:
    if file.content_type not in accepted_content_types:
        raise ValueError("File is not in an accepted content-type")

    file_rows = load_file(file)



    return TransactionCollection(transactions=[])
