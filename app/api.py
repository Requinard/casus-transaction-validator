from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI(
    title="ACME Transaction Validator"
)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("/docs")
