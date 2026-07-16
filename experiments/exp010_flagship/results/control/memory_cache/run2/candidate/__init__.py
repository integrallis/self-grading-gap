import time

class Cache:
    def __init__(self, capacity=100, ttl=60):
        if capacity < 1:
            raise ValueError(f"capacity must be at least 1, got [{capacity}]")
        if ttl <= 0:
            raise ValueError(f"ttl must be positive, got [{ttl}]")
        self.capacity = capacity
        self.ttl = ttl
        self.store = {}
        self.order = []

    def set(self, key, value):
        if key in self.store:
            self.store[key]['value'] = value
            self.store[key]['time'] = time.time()
            # Refresh recency in order
            self.order.remove(key)
            self.order.append(key)
        else:
            if len(self.store) >= self.capacity:
                self.evict()
            self.store[key] = {'value': value, 'time': time.time()}
            self.order.append(key)

    def get(self, key, default=None):
        if key in self.store:
            entry = self.store[key]
            if time.time() - entry['time'] < self.ttl:
                entry['time'] = time.time()  # Refresh recency
                return entry['value']
            else:
                del self.store[key]  # Expired
                self.order.remove(key)
        return default

    def remove(self, key):
        if key in self.store:
            del self.store[key]
            self.order.remove(key)
            return True
        return False

    def clear(self):
        self.store.clear()
        self.order.clear()

    def evict(self):
        while self.order:
            oldest_key = self.order.pop(0)
            if oldest_key in self.store:
                del self.store[oldest_key]
                break
