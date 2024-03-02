import pickle
from .leaky_bucket import LeakyBucket
from .singleton import Singleton

class LeakyBucketFactory(Singleton):
    def __init__(self, database_client, config: dict):
        self.lb_capacity = config["capacity"]
        self.lb_leak_rate = config["leak_rate"]
        self.database_client = database_client

    def __call__(self, ip):
        serialized_leaky_bucket = self.database_client.get(ip)
        if serialized_leaky_bucket:
            leaky_bucket = pickle.loads(serialized_leaky_bucket)
        else:
            leaky_bucket = LeakyBucket(self.lb_capacity, self.lb_leak_rate)
            serialized_leaky_bucket = pickle.dumps(leaky_bucket)
            self.database_client.set(ip, serialized_leaky_bucket)
        return leaky_bucket
    
    def save_leaky_bucket(self, ip, leaky_bucket):
        serialized_leaky_bucket = pickle.dumps(leaky_bucket)
        self.database_client.set(ip, serialized_leaky_bucket)
    