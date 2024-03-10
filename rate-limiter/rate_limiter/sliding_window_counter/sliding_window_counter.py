import time

class SlidingWindowCounter:
    
    def __init__(self, request_limit: int, window_size_in_seconds: int):
        self._validate_parameters(request_limit, window_size_in_seconds)
        self.request_limit = request_limit
        self.window_size_in_seconds = window_size_in_seconds
        self.timestamp_log = []
        
    def _validate_parameters(self, request_limit: int, window_size_in_seconds: int) -> None:
        if request_limit <= 0 or \
            window_size_in_seconds <= 0 or \
            not isinstance(request_limit, int) or \
            not isinstance(window_size_in_seconds, int):
                raise ValueError("request_limit and window_size_in_seconds should be natural numbers")

    def allow_request(self):
        current_time = int(time.time())
        self.timestamp_log = [timestamp for timestamp in self.timestamp_log \
                              if timestamp >= current_time - self.window_size_in_seconds]
        self.timestamp_log.append(current_time)
        if len(self.timestamp_log) <= self.request_limit:
            return True
        else:
            return False