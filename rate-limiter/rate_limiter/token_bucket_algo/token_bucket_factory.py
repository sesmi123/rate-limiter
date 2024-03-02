import pickle
from .token_bucket import TokenBucket
from .singleton import Singleton

class TokenBucketFactory(Singleton):
    def __init__(self, database_client, config: dict):
        self.tb_capacity = config["capacity"]
        self.tb_refill_amount = config["refill_amount"]
        self.tb_refill_time_in_seconds = config["refill_time_in_seconds"]
        self.database_client = database_client

    def __call__(self, ip):
        serialized_token_bucket = self.database_client.get(ip)
        if serialized_token_bucket:
            token_bucket = pickle.loads(serialized_token_bucket)
        else:
            token_bucket = TokenBucket(self.tb_capacity, 
                                        self.tb_refill_amount, 
                                        self.tb_refill_time_in_seconds)
            serialized_token_bucket = pickle.dumps(token_bucket)
            self.database_client.set(ip, serialized_token_bucket)
        return token_bucket
    
    def save_token_bucket(self, ip, token_bucket):
        serialized_token_bucket = pickle.dumps(token_bucket)
        self.database_client.set(ip, serialized_token_bucket)
    