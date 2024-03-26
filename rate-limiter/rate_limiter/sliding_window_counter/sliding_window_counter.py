from time import time

class SlidingWindowCounter:
    
    def __init__(self, request_limit: int, window_size_in_seconds: int):
        self._validate_parameters(request_limit, window_size_in_seconds)
        self.request_limit = request_limit
        self.window_size_in_seconds = window_size_in_seconds
        
        self.cur_time = int(time())
        self.cur_count = 0
        self.window = []
        
    def _validate_parameters(self, request_limit: int, window_size_in_seconds: int) -> None:
        if request_limit <= 0 or \
            window_size_in_seconds <= 0 or \
            not isinstance(request_limit, int) or \
            not isinstance(window_size_in_seconds, int):
                raise ValueError("request_limit and window_size_in_seconds should be natural numbers")

    def allow_request(self):
        # Check if it's a new time unit
        if (int(time()) - self.cur_time) > self.window_size_in_seconds:
            self.cur_time = int(time())
            self.window = [self.cur_count]
            self.cur_count = 0
        else:
            self.window.append(self.cur_count)

        effective_capacity = sum((self.request_limit - count) * \
                                (self.window_size_in_seconds - idx * self.window_size_in_seconds / len(self.window)) / \
                                self.window_size_in_seconds for idx, count in enumerate(self.window))
        
        # Check if the effective capacity is exceeded
        if effective_capacity > self.request_limit:
            return False

        self.cur_count += 1
        return True