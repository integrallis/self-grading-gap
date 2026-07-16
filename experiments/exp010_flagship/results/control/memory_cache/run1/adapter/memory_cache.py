# file: memory_cache.py
from candidate import Cache, time


_defaults = Cache()


class MemoryCache(Cache):
    put = Cache.set
    raises = Cache.has
    advance = time.sleep

    def __init__(self, capacity=_defaults.capacity, ttl=_defaults.ttl, *extra):
        Cache.__init__(self, capacity, ttl)
