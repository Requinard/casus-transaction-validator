import time
import uuid

from fastapi import FastAPI
from starlette.requests import Request

from transactions import router as TransactionsRouter

app = FastAPI(
    title="ACME Transaction Validator"
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def add_tracing_header(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    return response

app.include_router(
    TransactionsRouter,
    tags=["Transactions"]
)
