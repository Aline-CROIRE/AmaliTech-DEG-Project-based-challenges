from fastapi import FastAPI
from app.api.payment_routes import router as payment_router

app = FastAPI(
    title="FinSafe Idempotency Gateway",
    description=(
        "A concurrency-safe Idempotency Layer API built with FastAPI. "
        "Ensures payment requests with the same Idempotency-Key execute exactly once."
    ),
    version="1.0.0",
    docs_url="/docs",      
    redoc_url="/redoc"     
)


app.include_router(payment_router)

