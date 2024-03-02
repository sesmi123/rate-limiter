import threading
from functools import wraps
from flask import jsonify, request


class TokenBucketRateLimiter:

    def __init__(self, token_bucket_factory) -> None:
        self.token_bucket_factory = token_bucket_factory
        self.token_bucket_lock = threading.Lock()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ip = request.remote_addr
            token_bucket = self.token_bucket_factory(ip)
            with self.token_bucket_lock:
                if token_bucket.consume_token():
                    self.token_bucket_factory.save_token_bucket(ip, token_bucket)
                    return func(*args, **kwargs)
                else:
                    return jsonify({"error": "Rate limit exceeded"}), 429 
        return wrapper
