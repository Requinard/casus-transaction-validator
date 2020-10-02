from fastapi import FastAPI

from transactions import router as TransactionsRouter

app = FastAPI(
    title="ACME Transaction Validator"
)

app.include_router(
    TransactionsRouter,
    tags=["Transactions"]
)
