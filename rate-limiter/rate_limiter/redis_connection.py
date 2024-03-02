import redis

class RedisConnection:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.redis_client = None

    def connect(self):
        self.redis_client = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

    def set(self, key, value):
        self.redis_client.set(key, value)

    def get(self, key):
        return self.redis_client.get(key)