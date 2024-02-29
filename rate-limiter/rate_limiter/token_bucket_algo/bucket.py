
from typing import Any

class Bucket():
    
    def __init__(self, capacity) -> None:
        self._validate_bucket_parameters(capacity)
        self.capacity = capacity
        self.my_bucket = list()
    
    def _validate_bucket_parameters(self, capacity: int) -> None:
        
        if capacity <= 0 or not isinstance(capacity, int):
                raise ValueError("capacity should be a natural number")
    
    def fill_level(self) -> int:
         return len(self.my_bucket)
         
    def is_full(self):
        return self.fill_level() == self.capacity

    def is_empty(self):
        return self.fill_level() == 0

    def fill(self, items: list) -> None:
        for item in items:
            if self.is_full():
                break
            self.my_bucket.append(item)

    def empty(self) -> Any:
        if not self.is_empty():
            return self.my_bucket.pop()
