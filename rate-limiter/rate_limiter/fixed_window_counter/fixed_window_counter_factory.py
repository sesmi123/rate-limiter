import pickle
from .singleton import Singleton
from .fixed_window_counter import FixedWindowCounter

class FixedWindowCounterFactory(Singleton):

    def __init__(self, database_client, config: dict):
        self.request_limit = config["request_limit"]
        self.window_size = config["window_size"]
        self.database_client = database_client
        self._db_key = "my_fixed_window_counter"

    def __call__(self):
        serialized_fwc = self.database_client.get(self._db_key)
        if serialized_fwc:
            fwc = pickle.loads(serialized_fwc)
        else:
            fwc = FixedWindowCounter(self.request_limit, self.window_size)
            serialized_fwc = pickle.dumps(fwc)
            self.database_client.set(self._db_key, serialized_fwc)
        return fwc
    
    def save_fixed_window_counter(self, fixed_window_counter):
        serialized_fwc = pickle.dumps(fixed_window_counter)
        self.database_client.set(self._db_key, serialized_fwc)
    