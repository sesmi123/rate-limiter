from .token_bucket import TokenBucket
from .singleton import Singleton

class TokenBucketFactory(Singleton):
    def __init__(self, config: dict):
        self.tb_capacity = config["capacity"]
        self.tb_refill_amount = config["refill_amount"]
        self.tb_refill_time_in_seconds = config["refill_time_in_seconds"]
        self.token_buckets = {}

    def __call__(self, ip):
        if ip not in self.token_buckets:
            self.token_buckets[ip] = TokenBucket(self.tb_capacity, 
                                                 self.tb_refill_amount, 
                                                 self.tb_refill_time_in_seconds)
        return self.token_buckets[ip]
    