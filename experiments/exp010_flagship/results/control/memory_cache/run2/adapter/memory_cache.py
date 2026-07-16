# file: memory_cache.py
from candidate import Cache as MemoryCache

MemoryCache.put = MemoryCache.set
MemoryCache.sweep = MemoryCache.evict
