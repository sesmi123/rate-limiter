import time

class FixedWindowCounter:
    def __init__(self, request_limit: int, window_size_in_seconds: int):
        self._validate_parameters(request_limit, window_size_in_seconds)
        self.request_limit = request_limit
        self.window_size_in_seconds = window_size_in_seconds
        self.window_start_time = int(time.time())
        self.request_count = 0
        
    def _validate_parameters(self, request_limit: int, window_size_in_seconds: int) -> None:
        if request_limit <= 0 or \
            window_size_in_seconds <= 0 or \
            not isinstance(request_limit, int) or \
            not isinstance(window_size_in_seconds, int):
                raise ValueError("request_limit and window_size_in_seconds should be natural numbers")

    def allow_request(self):
        current_time = int(time.time())
        if current_time >= self.window_start_time + self.window_size_in_seconds:
            # If current time is beyond the current window, reset the counter and start a new window
            self.window_start_time = current_time
            self.request_count = 0
        
        if self.request_count < self.request_limit:
            self.request_count += 1
            return True
        else:
            return False