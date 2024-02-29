
import threading
import time
from .bucket import Bucket


class Token():
    pass

class TokenBucket():

    def __init__(self, capacity: int, refill_amount: int, refill_time_in_seconds: int) -> None:
        self._my_bucket = Bucket(capacity)
        self._validate_parameters( refill_amount, refill_time_in_seconds)
        self._my_bucket.fill([Token() for _ in range(capacity)])
        self.refill_amount = refill_amount
        self.refill_time_in_seconds = refill_time_in_seconds
        self.last_refill_time = int(time.time())
        self.refill_rate = self.refill_amount / self.refill_time_in_seconds
        self.lock = threading.Lock()

    def _validate_parameters(self, refill_amount: int, refill_time_in_seconds: int) -> None:
        if refill_amount <= 0 or \
            refill_time_in_seconds <= 0 or \
            not isinstance(refill_amount, int) or \
            not isinstance(refill_time_in_seconds, int):
                raise ValueError("refill_amount and refill_time_in_seconds should be natural numbers")

    def _refill_tokens(self) -> None:
        current_time = int(time.time())
        time_elapsed_in_seconds = current_time - self.last_refill_time
        if time_elapsed_in_seconds >= self.refill_time_in_seconds:
            number_of_tokens_to_add = (time_elapsed_in_seconds//self.refill_time_in_seconds) * self.refill_amount
            self._my_bucket.fill([Token() for _ in range(number_of_tokens_to_add)])
            self.last_refill_time = current_time
    
    def _pop_token(self) -> bool:
        if self._my_bucket.is_empty():
            raise ValueError("Bucket is already empty")
        
        self._my_bucket.empty()
        return True

    def _available_tokens(self) -> int:
        self._refill_tokens()
        return self._my_bucket.fill_level()
    
    def consume_token(self) -> bool:
        if self._available_tokens() > 0:
            self._pop_token()
            return True
        else:
            return False