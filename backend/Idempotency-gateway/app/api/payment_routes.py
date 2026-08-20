from fastapi import APIRouter, Header, HTTPException, status, Response
from app.schemas.payment import PaymentRequest, PaymentResponse, ErrorResponse
from app.services.payment_service import payment_service
from app.services.idempotency_service import idempotency_service
from app.core.exceptions import IdempotencyConflictException

router = APIRouter(tags=["Payments"])


@router.post(
    "/process-payment",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
    summary="Process a Payment",
    description="Processes a payment transaction with idempotency protection.",
    responses={
        200: {
            "description": "Payment processed successfully.",
            "model": PaymentResponse,
            "headers": {
                "X-Cache-Hit": {
                    "description": "Indicates if response was served from cache",
                    "schema": {"type": "boolean"}
                }
            }
        },
        400: {"description": "Missing or invalid Idempotency-Key header", "model": ErrorResponse},
        409: {"description": "Idempotency key reused for a different payload", "model": ErrorResponse},
        422: {"description": "Validation error", "model": ErrorResponse}
    }
)
async def process_payment(
    payment_data: PaymentRequest,
    response: Response,
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key",
        description="Unique string identifying this payment attempt.",
        examples=["req_unique_key_001"]
    )
):
    if not idempotency_key or not idempotency_key.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Header 'Idempotency-Key' cannot be empty."
        )

    payload_dict = payment_data.model_dump()

    async def execute_payment():
        payment_result = await payment_service.process_payment(
            amount=payment_data.amount,
            currency=payment_data.currency
        )
        return payment_result.model_dump(), status.HTTP_200_OK

    try:
        result_body, status_code, is_cache_hit = await idempotency_service.execute_idempotent(
            key=idempotency_key.strip(),
            payload=payload_dict,
            action_coroutine=execute_payment
        )

        response.headers["X-Cache-Hit"] = "true" if is_cache_hit else "false"
        response.status_code = status_code
        return result_body

    except IdempotencyConflictException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.message
        )