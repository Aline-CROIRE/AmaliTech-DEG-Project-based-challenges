import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.storage.idempotency_store import idempotency_store


@pytest.fixture(autouse=True)
def clear_store():
    idempotency_store.clear()


@pytest.mark.asyncio
async def test_first_payment_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/process-payment",
            headers={"Idempotency-Key": "key-001"},
            json={"amount": 100, "currency": "RWF"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Charged 100 RWF"
        assert data["amount"] == 100.0
        assert data["currency"] == "RWF"
        assert "transaction_id" in data
        assert response.headers.get("x-cache-hit") == "false"


@pytest.mark.asyncio
async def test_missing_idempotency_key():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/process-payment",
            json={"amount": 100, "currency": "RWF"}
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_empty_idempotency_key():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/process-payment",
            headers={"Idempotency-Key": "   "},
            json={"amount": 100, "currency": "RWF"}
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_invalid_amount_negative():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/process-payment",
            headers={"Idempotency-Key": "key-002"},
            json={"amount": -50, "currency": "RWF"}
        )
        assert response.status_code == 422