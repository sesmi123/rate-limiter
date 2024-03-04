
import time
from .bucket import Bucket


class Token():
    pass

class LeakyBucket():

    def __init__(self, capacity: int, leak_rate: float) -> None:
        self._my_bucket = Bucket(capacity)
        self._validate_parameters(leak_rate)
        self.leak_rate = leak_rate
        self.last_leak_time = int(time.time())

    def _validate_parameters(self, leak_rate: float) -> None:
        if leak_rate <= 0 or \
            not isinstance(leak_rate, float):
                raise ValueError("leak_rate should be a float")

    
    def _leak(self):
        current_time = int(time.time())
        time_elapsed_in_seconds = current_time - self.last_leak_time
        self.last_leak_time = current_time
        number_of_tokens_to_leak = int(time_elapsed_in_seconds * self.leak_rate) % self._my_bucket.capacity
        for _ in range(number_of_tokens_to_leak):
            self._my_bucket.empty()
        
    def _fill(self):
        self._my_bucket.fill([Token()])

    def _has_capacity(self) -> bool:
        if self._my_bucket.is_full():
            return False
        return True

    def allow_request(self):
        self._leak()
        if self._has_capacity():
            self._fill()
            return True
        return False