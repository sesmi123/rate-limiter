
import threading
import time
from .bucket import Bucket


class Token():
    pass

class TokenBucket(Bucket):

    def __init__(self, capacity: int, refill_amount: int, refill_time_in_seconds: int) -> None:
        super().__init__(capacity)
        self._validate_token_bucket_parameters( refill_amount, refill_time_in_seconds)
        self.fill([Token() for _ in range(capacity)])
        self.refill_amount = refill_amount
        self.refill_time_in_seconds = refill_time_in_seconds
        self.last_refill_time = int(time.time())
        self.refill_rate = self.refill_amount / self.refill_time_in_seconds
        self.lock = threading.Lock()

    def _validate_token_bucket_parameters(self, refill_amount: int, refill_time_in_seconds: int) -> None:
        if refill_amount <= 0 or \
            refill_time_in_seconds <= 0 or \
            not isinstance(refill_amount, int) or \
            not isinstance(refill_time_in_seconds, int):
                raise ValueError("refill_amount and refill_time_in_seconds should be natural numbers")

    def refill_tokens(self):
        current_time = int(time.time())
        time_elapsed_in_seconds = current_time - self.last_refill_time
        if time_elapsed_in_seconds >= self.refill_time_in_seconds:
            number_of_tokens_to_add = (time_elapsed_in_seconds//self.refill_time_in_seconds) * self.refill_amount
            self.fill([Token() for _ in range(number_of_tokens_to_add)])
            self.last_refill_time = current_time
    
    def pop_token(self) -> bool:
        if self.is_empty():
            raise ValueError("Bucket is already empty")
        
        with self.lock:
            super().empty()
            return True
