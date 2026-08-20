from fastapi import APIRouter, Header, HTTPException, status, Response
from app.schemas.payment import PaymentRequest, PaymentResponse, ErrorResponse
from app.services.payment_service import payment_service

router = APIRouter(tags=["Payments"])


@router.post(
    "/process-payment",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
    summary="Process a Payment",
    description="Processes a payment transaction. Requires an 'Idempotency-Key' header.",
    responses={
        200: {
            "description": "Payment processed successfully.",
            "model": PaymentResponse,
            "headers": {
                "X-Cache-Hit": {
                    "description": "Indicates if the response was served from idempotency cache",
                    "schema": {"type": "boolean", "example": False}
                }
            }
        },
        400: {"description": "Missing or invalid Idempotency-Key header", "model": ErrorResponse},
        409: {"description": "Idempotency key reused with a different payload", "model": ErrorResponse},
        422: {"description": "Validation error (invalid amount or currency)", "model": ErrorResponse}
    }
)
async def process_payment(
    payment_data: PaymentRequest,
    response: Response,
    idempotency_key: str = Header(
        alias="Idempotency-Key",
        description="Unique UUID or string identifying this idempotency request attempt.",
        examples=["req_unique_key_001"]
    )
):
   
    if not idempotency_key or not idempotency_key.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Header 'Idempotency-Key' cannot be empty."
        )

    result = await payment_service.process_payment(
        amount=payment_data.amount,
        currency=payment_data.currency
    )

   
    response.headers["X-Cache-Hit"] = "false"
    return result