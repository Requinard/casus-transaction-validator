from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI(
    title="ACME Transaction Validator"
)


@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")
