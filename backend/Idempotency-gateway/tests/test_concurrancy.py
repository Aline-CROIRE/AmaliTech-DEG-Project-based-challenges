import pytest
import asyncio
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.payment_service import payment_service
from app.storage.idempotency_store import idempotency_store


@pytest.fixture(autouse=True)
def clear_store():
    idempotency_store.clear()


@pytest.mark.asyncio
async def test_concurrent_in_flight_requests_executed_once():
    execution_counter = 0
    original_process = payment_service.process_payment

    async def mock_process(amount: float, currency: str):
        nonlocal execution_counter
        execution_counter += 1
        return await original_process(amount, currency)

    with patch.object(payment_service, "process_payment", side_effect=mock_process):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            headers = {"Idempotency-Key": "concurrent-key-999"}
            payload = {"amount": 300, "currency": "RWF"}

            tasks = [
                client.post("/process-payment", headers=headers, json=payload)
                for _ in range(5)
            ]

            responses = await asyncio.gather(*tasks)

            for response in responses:
                assert response.status_code == 200
                assert response.json()["amount"] == 300.0

            cache_hits = [r.headers.get("x-cache-hit") for r in responses]
            assert cache_hits.count("false") == 1
            assert cache_hits.count("true") == 4

            first_tx_id = responses[0].json()["transaction_id"]
            for r in responses:
                assert r.json()["transaction_id"] == first_tx_id

            assert execution_counter == 1