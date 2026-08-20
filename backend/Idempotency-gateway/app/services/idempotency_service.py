import json
import hashlib
from typing import Dict, Any, Tuple
from app.storage.idempotency_store import InMemoryIdempotencyStore, IdempotencyRecord, idempotency_store
from app.core.exceptions import IdempotencyConflictException


class IdempotencyService:
    def __init__(self, store: InMemoryIdempotencyStore):
        self.store = store

    def generate_fingerprint(self, payload: Dict[str, Any]) -> str:
        canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    async def execute_idempotent(
        self,
        key: str,
        payload: Dict[str, Any],
        action_coroutine
    ) -> Tuple[Dict[str, Any], int, bool]:
        fingerprint = self.generate_fingerprint(payload)
        existing_record = self.store.get(key)

        if existing_record:
            if existing_record.fingerprint != fingerprint:
                raise IdempotencyConflictException()

            if existing_record.status == "COMPLETED":
                return existing_record.response_body, existing_record.status_code, True

            if existing_record.status == "PENDING":
                await existing_record.event.wait()
                updated_record = self.store.get(key)
                if updated_record and updated_record.status == "COMPLETED":
                    return updated_record.response_body, updated_record.status_code, True
                else:
                    raise Exception("In-flight operation failed.")

        new_record = IdempotencyRecord(
            key=key,
            fingerprint=fingerprint,
            status="PENDING"
        )
        self.store.save(new_record)

        try:
            result_body, status_code = await action_coroutine()
            new_record.response_body = result_body
            new_record.status_code = status_code
            new_record.status = "COMPLETED"
            self.store.save(new_record)
            return result_body, status_code, False
        except Exception as exc:
            self.store.delete(key)
            raise exc
        finally:
            new_record.event.set()


idempotency_service = IdempotencyService(store=idempotency_store)