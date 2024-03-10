import pickle
from .singleton import Singleton
from .sliding_window_counter import SlidingWindowCounter

class SlidingWindowCounterFactory(Singleton):

    def __init__(self, database_client, config: dict):
        self.request_limit = config["request_limit"]
        self.window_size = config["window_size"]
        self.database_client = database_client
        self._db_key = "my_sliding_window_counter"

    def __call__(self):
        serialized_swc = self.database_client.get(self._db_key)
        if serialized_swc:
            swc = pickle.loads(serialized_swc)
        else:
            swc = SlidingWindowCounter(self.request_limit, self.window_size)
            serialized_swc = pickle.dumps(swc)
            self.database_client.set(self._db_key, serialized_swc)
        return swc
    
    def save_sliding_window_counter(self, sliding_window_counter):
        serialized_swc = pickle.dumps(sliding_window_counter)
        self.database_client.set(self._db_key, serialized_swc)
    