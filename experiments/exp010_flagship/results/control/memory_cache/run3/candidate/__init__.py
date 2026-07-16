import time
from collections import OrderedDict

class Cache:
    def __init__(self, capacity=100, ttl=60):
        if capacity < 1:
            raise ValueError(f"capacity must be at least 1, got [{capacity}]")
        if ttl <= 0:
            raise ValueError(f"ttl must be positive, got [{ttl}]")
        self.capacity = capacity
        self.ttl = ttl
        self.store = OrderedDict()

    def _is_expired(self, timestamp):
        return time.time() - timestamp > self.ttl

    def add(self, key, value):
        current_time = time.time()
        if key in self.store:
            # Update existing key
            self.store.move_to_end(key)
            self.store[key] = (value, current_time)
        else:
            if len(self.store) >= self.capacity:
                # Evict the least recently used item
                self.store.popitem(last=False)
            self.store[key] = (value, current_time)

    def retrieve(self, key, fallback=None):
        if key in self.store:
            value, timestamp = self.store[key]
            if self._is_expired(timestamp):
                self.store.pop(key)
                return None
            self.store.move_to_end(key)
            return value
        return fallback

    def remove(self, key):
        if key in self.store:
            del self.store[key]
            return True
        return False

    def count(self):
        self.sweep()
        return len(self.store)

    def sweep(self):
        stale_keys = [key for key, (value, timestamp) in self.store.items() if self._is_expired(timestamp)]
        for key in stale_keys:
            del self.store[key]
        return len(stale_keys)

    def clear(self):
        self.store.clear()

    def __contains__(self, key):
        return key in self.store and not self._is_expired(self.store[key][1])
