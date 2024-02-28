
class Token():
    pass


class TokenBucket():

    def __init__(self, capacity: int, 
        refill_amount: int, 
        refill_time_in_seconds: int) -> None:
            
            self._validate_constructor_parameters(capacity, 
                refill_amount, 
                refill_time_in_seconds)
            self.my_bucket = []
            self.capacity = capacity
            self.fill_level = capacity
            self.fill(capacity)
            self.refill_amount = refill_amount
            self.refill_time_in_seconds = refill_time_in_seconds

    def _validate_constructor_parameters(self, 
        capacity: int, 
        refill_amount: int, 
        refill_time_in_seconds: int) -> None:
            
            if capacity <= 0 or refill_amount <= 0 or \
                refill_time_in_seconds <= 0 or \
                not isinstance(capacity, int) or \
                not isinstance(refill_amount, int) or \
                not isinstance(refill_time_in_seconds, int):
                    raise ValueError("capacity, refill_amount, and refill_time_in_seconds should be natural numbers.")

    def is_full(self):
        return len(self.my_bucket) == self.capacity

    def is_empty(self):
        return len(self.my_bucket) == 0

    def fill(self, amount: int) -> None:
        for _ in range(amount):
            if not self.is_full():
                self.my_bucket.append(Token())

    def empty(self, amount: int) -> None:
        if amount > len(self.my_bucket):
            raise ValueError("Cannot empty more tokens than available in the bucket.")
        for _ in range(amount):
            if not self.is_empty():
                self.my_bucket.pop()