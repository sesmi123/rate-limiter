import pickle
from .singleton import Singleton
from .sliding_window_log import SlidingWindowLog

class SlidingWindowLogFactory(Singleton):

    def __init__(self, database_client, config: dict):
        self.request_limit = config["request_limit"]
        self.window_size = config["window_size"]
        self.database_client = database_client
        self._db_key = "my_sliding_window_log"

    def __call__(self):
        serialized_swl = self.database_client.get(self._db_key)
        if serialized_swl:
            swl = pickle.loads(serialized_swl)
        else:
            swl = SlidingWindowLog(self.request_limit, self.window_size)
            serialized_swl = pickle.dumps(swl)
            self.database_client.set(self._db_key, serialized_swl)
        return swl
    
    def save_sliding_window_log(self, sliding_window_log):
        serialized_swl = pickle.dumps(sliding_window_log)
        self.database_client.set(self._db_key, serialized_swl)
    