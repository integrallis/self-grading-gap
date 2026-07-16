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
        self.cache = OrderedDict()

    def set(self, key, value):
        current_time = time.time()
        if key in self.cache:
            # Update existing key
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Evict least recently used (LRU) item
            self.cache.popitem(last=False)
        self.cache[key] = (value, current_time)

    def get(self, key, fallback=None):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                self.cache.move_to_end(key)
                return value
            else:
                del self.cache[key]  # Remove expired entry
        return fallback

    def remove(self, key):
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def count(self):
        self.sweep()  # Clean up expired entries
        return len(self.cache)

    def has(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return True
            else:
                del self.cache[key]  # Remove expired entry
        return False

    def clear(self):
        self.cache.clear()

    def sweep(self):
        current_time = time.time()
        removed_count = 0
        for key in list(self.cache.keys()):
            value, timestamp = self.cache[key]
            if current_time - timestamp >= self.ttl:
                del self.cache[key]
                removed_count += 1
        return removed_count

    def __repr__(self):
        return f"Cache(capacity={self.capacity}, ttl={self.ttl})"