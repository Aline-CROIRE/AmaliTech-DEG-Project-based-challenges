import asyncio
import uuid
from app.schemas.payment import PaymentResponse


class PaymentService:
    async def process_payment(self, amount: float, currency: str) -> PaymentResponse:
        await asyncio.sleep(2.0)

        tx_id = f"tx_{uuid.uuid4().hex[:10]}"
        message = f"Charged {int(amount) if amount.is_integer() else amount} {currency}"

        return PaymentResponse(
            message=message,
            amount=amount,
            currency=currency,
            transaction_id=tx_id,
            status="SUCCESS"
        )


payment_service = PaymentService()