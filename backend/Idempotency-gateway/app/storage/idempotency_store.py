import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any


@dataclass
class IdempotencyRecord:
    key: str
    fingerprint: str
    status: str
    response_body: Optional[Dict[str, Any]] = None
    status_code: Optional[int] = None
    event: asyncio.Event = field(default_factory=asyncio.Event)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class InMemoryIdempotencyStore:
    def __init__(self, ttl_seconds: int = 86400):
        self._store: Dict[str, IdempotencyRecord] = {}
        self.ttl_seconds = ttl_seconds

    def get(self, key: str) -> Optional[IdempotencyRecord]:
        record = self._store.get(key)
        if not record:
            return None

        now = datetime.now(timezone.utc)
        elapsed = (now - record.created_at).total_seconds()
        if elapsed > self.ttl_seconds:
            del self._store[key]
            return None

        return record

    def save(self, record: IdempotencyRecord) -> None:
        self._store[record.key] = record

    def delete(self, key: str) -> None:
        if key in self._store:
            del self._store[key]

    def clear(self) -> None:
        self._store.clear()


idempotency_store = InMemoryIdempotencyStore()