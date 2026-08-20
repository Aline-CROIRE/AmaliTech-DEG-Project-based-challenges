import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.storage.idempotency_store import idempotency_store


@pytest.fixture(autouse=True)
def clear_store():
    idempotency_store.clear()


@pytest.mark.asyncio
async def test_duplicate_request_returns_cached_response():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {"amount": 250, "currency": "USD"}
        headers = {"Idempotency-Key": "dup-key-100"}

        res1 = await client.post("/process-payment", headers=headers, json=payload)
        assert res1.status_code == 200
        assert res1.headers.get("x-cache-hit") == "false"

        res2 = await client.post("/process-payment", headers=headers, json=payload)
        assert res2.status_code == 200
        assert res2.headers.get("x-cache-hit") == "true"
        assert res1.json() == res2.json()


@pytest.mark.asyncio
async def test_same_key_different_body_returns_conflict():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Idempotency-Key": "conflict-key-100"}

        res1 = await client.post(
            "/process-payment",
            headers=headers,
            json={"amount": 100, "currency": "RWF"}
        )
        assert res1.status_code == 200

        res2 = await client.post(
            "/process-payment",
            headers=headers,
            json={"amount": 500, "currency": "RWF"}
        )
        assert res2.status_code == 409
        assert res2.json()["detail"] == "Idempotency key already used for a different request body."


@pytest.mark.asyncio
async def test_key_ttl_expiration():
    idempotency_store.ttl_seconds = 1
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {"Idempotency-Key": "ttl-key-100"}
        payload = {"amount": 75, "currency": "EUR"}

        res1 = await client.post("/process-payment", headers=headers, json=payload)
        assert res1.status_code == 200
        tx1 = res1.json()["transaction_id"]

        await asyncio.sleep(1.1)

        res2 = await client.post("/process-payment", headers=headers, json=payload)
        assert res2.status_code == 200
        assert res2.headers.get("x-cache-hit") == "false"
        tx2 = res2.json()["transaction_id"]
        assert tx1 != tx2

    idempotency_store.ttl_seconds = 86400