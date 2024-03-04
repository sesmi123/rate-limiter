import time

class FixedWindowCounter:
    def __init__(self, request_limit: int, window_size_in_seconds: int):
        self._validate_parameters(request_limit, window_size_in_seconds)
        self.request_limit = request_limit
        self.window_size_in_seconds = window_size_in_seconds
        self.requests_in_window = []
        
    def _validate_parameters(self, request_limit: int, window_size_in_seconds: int) -> None:
        if request_limit <= 0 or \
            window_size_in_seconds <= 0 or \
            not isinstance(request_limit, int) or \
            not isinstance(window_size_in_seconds, int):
                raise ValueError("request_limit and window_size_in_seconds should be natural numbers")

    def allow_request(self):
        current_time = int(time.time())
        
        # Remove requests from the window that are older than the window_size
        self.requests_in_window = [req_time for req_time in self.requests_in_window \
                                   if req_time > current_time - self.window_size_in_seconds]
        
        # Check if the number of requests in the window exceeds the limit
        if len(self.requests_in_window) < self.request_limit:
            self.requests_in_window.append(current_time)
            return True
        else:
            return False