from pydantic import BaseModel, Field, field_validator


class PaymentRequest(BaseModel):
    amount: float = Field(
        ...,
        gt=0,
        description="The payment amount (must be greater than 0)",
        examples=[100.00]
    )
    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="3-letter ISO currency code (e.g. GHS, USD)",
        examples=["GHS"]
    )

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        return v.upper().strip()

    model_config = {
        "json_schema_extra": {
            "example": {
                "amount": 100.00,
                "currency": "GHS"
            }
        }
    }


class PaymentResponse(BaseModel):
    message: str = Field(description="Human-readable status message", examples=["Charged 100 GHS"])
    amount: float = Field(examples=[100.00])
    currency: str = Field(examples=["GHS"])
    transaction_id: str = Field(description="Unique payment transaction ID", examples=["tx_abc12345"])
    status: str = Field(description="Transaction status", examples=["SUCCESS"])


class ErrorResponse(BaseModel):
    detail: str = Field(description="Error message explaining the failure")