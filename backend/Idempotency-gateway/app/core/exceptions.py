class IdempotencyConflictException(Exception):
    def __init__(self, message: str = "Idempotency key already used for a different request body."):
        self.message = message
        super().__init__(self.message)


class InvalidIdempotencyKeyException(Exception):
    def __init__(self, message: str = "Header 'Idempotency-Key' is missing or invalid."):
        self.message = message
        super().__init__(self.message)