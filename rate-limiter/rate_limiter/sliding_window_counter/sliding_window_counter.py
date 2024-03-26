from time import time

class SlidingWindowCounter:
    
    def __init__(self, request_limit: int, window_size_in_seconds: int):
        self._validate_parameters(request_limit, window_size_in_seconds)
        self.request_limit = request_limit
        self.window_size_in_seconds = window_size_in_seconds
        
        self.current_window_start = int(time())
        self.current_window_request_count = 0
        self.previous_window_start = int(time()) - window_size_in_seconds
        self.previous_window_request_count = 0
        
    def _validate_parameters(self, request_limit: int, window_size_in_seconds: int) -> None:
        if request_limit <= 0 or \
            window_size_in_seconds <= 0 or \
            not isinstance(request_limit, int) or \
            not isinstance(window_size_in_seconds, int):
                raise ValueError("request_limit and window_size_in_seconds should be natural numbers")

    def allow_request(self):
        current_time = int(time())
        if self.current_window_start + self.window_size_in_seconds > current_time:
            # We are within the current window
            prev_window_weight = ( self.current_window_start - (current_time - self.window_size_in_seconds) ) / self.window_size_in_seconds
            effective_capacity = self.current_window_request_count + 1 + prev_window_weight * self.previous_window_request_count
            if effective_capacity > self.request_limit:
                return False
            else:
                self.current_window_request_count += 1
                return True
        else:
            # We are in a new window
            if self.current_window_start + 2 * self.window_size_in_seconds > current_time:
                # New window is adjacent to current window
                self.previous_window_request_count = self.current_window_request_count
                self.previous_window_start = self.current_window_start
                self.current_window_request_count = 1
                self.current_window_start = self.previous_window_start + self.window_size_in_seconds
                return True
            else:
                # New window is not adjacent to the current window
                # self.current_window_start = current_time
                n = int((current_time - self.current_window_start)/self.window_size_in_seconds)
                self.current_window_start = self.current_window_start + self.window_size_in_seconds * n
                self.current_window_request_count = 1
                self.previous_window_start = self.current_window_start - self.window_size_in_seconds
                self.previous_window_request_count = 0
                return True