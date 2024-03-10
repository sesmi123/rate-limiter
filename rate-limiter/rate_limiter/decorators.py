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

class LeakyBucketRateLimiter:

    def __init__(self, leaky_bucket_factory) -> None:
        self.leaky_bucket_factory = leaky_bucket_factory
        self.leaky_bucket_lock = threading.Lock()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ip = request.remote_addr
            leaky_bucket = self.leaky_bucket_factory(ip)
            with self.leaky_bucket_lock:
                if leaky_bucket.allow_request():
                    self.leaky_bucket_factory.save_leaky_bucket(ip, leaky_bucket)
                    return func(*args, **kwargs)
                else:
                    return jsonify({"error": "Rate limit exceeded"}), 429 
        return wrapper

class FixedWindowCounterRateLimiter:

    def __init__(self, fwc_factory) -> None:
        self.fwc_factory = fwc_factory
        self.fwc_lock = threading.Lock()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            fwc = self.fwc_factory()
            with self.fwc_lock:
                if fwc.allow_request():
                    self.fwc_factory.save_fixed_window_counter(fwc)
                    return func(*args, **kwargs)
                else:
                    return jsonify({"error": "Rate limit exceeded"}), 429 
        return wrapper

class SlidingWindowLogRateLimiter:

    def __init__(self, swl_factory) -> None:
        self.swl_factory = swl_factory
        self.swl_lock = threading.Lock()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            swl = self.swl_factory()
            with self.swl_lock:
                if swl.allow_request():
                    self.swl_factory.save_sliding_window_log(swl)
                    return func(*args, **kwargs)
                else:
                    return jsonify({"error": "Rate limit exceeded"}), 429 
        return wrapper

