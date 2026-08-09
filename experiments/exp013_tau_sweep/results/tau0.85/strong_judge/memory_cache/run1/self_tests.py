import pytest

from solution import Cache

def test_default_capacity_and_ttl():
    cache = Cache()
    # Default capacity is 100
    assert cache.capacity == 100
    # Default TTL is 60 seconds
    assert cache.ttl == 60

def test_configurable_capacity_and_ttl():
    cache = Cache(capacity=50, ttl=30)
    assert cache.capacity == 50
    assert cache.ttl == 30

def test_capacity_below_one_rejected():
    with pytest.raises(ValueError, match=r"^capacity must be at least 1, got \[-1\]$"):
        Cache(capacity=-1)
    with pytest.raises(ValueError, match=r"^capacity must be at least 1, got \[0\]$"):
        Cache(capacity=0)

def test_ttl_zero_or_negative_rejected():
    with pytest.raises(ValueError, match=r"^ttl must be positive, got \[-1\]$"):
        Cache(ttl=-1)
    with pytest.raises(ValueError, match=r"^ttl must be positive, got \[0\]$"):
        Cache(ttl=0)

def test_ttl_positive_accepted():
    cache = Cache(ttl=1)
    assert cache.ttl == 1

def test_ttl_fractional_positive_accepted():
    cache = Cache(ttl=0.5)
    assert cache.ttl == 0.5

def test_store_and_retrieve():
    cache = Cache()
    cache.store("key1", "value1")
    assert cache.retrieve("key1") == "value1"  # should return the stored value

def test_retrieve_absent_key():
    cache = Cache()
    assert cache.retrieve("absent_key") is None  # should return None by default
    assert cache.retrieve("absent_key", fallback="fallback_value") == "fallback_value"  # fallback value

def test_store_existing_key_replaces_value():
    cache = Cache()
    cache.store("key1", "value1")
    cache.store("key1", "value2")
    assert cache.retrieve("key1") == "value2"  # should return the new value

def test_store_existing_key_does_not_increase_count():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key1", "value2")
    assert cache.count() == 1  # count should remain 1

def test_lru_eviction():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key3", "value3")  # key1 should be evicted
    assert cache.retrieve("key1") is None  # key1 should be absent
    assert cache.retrieve("key2") == "value2"  # key2 should be present
    assert cache.retrieve("key3") == "value3"  # key3 should be present

def test_reading_refreshes_recency():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.retrieve("key1")  # refresh key1
    cache.store("key3", "value3")  # key2 should be evicted
    assert cache.retrieve("key2") is None  # key2 should be absent
    assert cache.retrieve("key1") == "value1"  # key1 should be present
    assert cache.retrieve("key3") == "value3"  # key3 should be present

def test_rewriting_key_refreshes_ttl():
    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)
    cache.store("key1", "value1")
    clock.advance(0.5)  # advance time by half a second
    cache.store("key1", "value2")  # rewrite key1
    clock.advance(0.5)  # advance time to 1 second
    assert cache.retrieve("key1") == "value2"  # should return the new value

def test_expiry_of_entries():
    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)
    cache.store("key1", "value1")
    clock.advance(1)  # advance time by 1 second
    assert cache.retrieve("key1") is None  # key1 should be absent

def test_expiry_boundary():
    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)
    cache.store("key1", "value1")
    assert cache.retrieve("key1") == "value1"  # should be present before expiry
    clock.advance(1)  # advance time to the expiry boundary
    assert cache.retrieve("key1") is None  # should be absent after expiry

def test_sweep_removes_stale_entries():
    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    clock.advance(1)  # advance time to expire key1
    removed_count = cache.sweep()  # should remove key1
    assert removed_count == 1  # one stale entry should be removed
    assert cache.retrieve("key1") is None  # key1 should be absent
    assert cache.retrieve("key2") == "value2"  # key2 should still be present

def test_sweep_with_multiple_stale_entries():
    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key3", "value3")
    clock.advance(1)  # advance time to expire all keys
    removed_count = cache.sweep()  # should remove all keys
    assert removed_count == 3  # all entries should be removed
    assert cache.retrieve("key1") is None  # key1 should be absent
    assert cache.retrieve("key2") is None  # key2 should be absent
    assert cache.retrieve("key3") is None  # key3 should be absent

def test_insertion_into_full_cache_reclaims_stale_entries():
    clock = FakeClock()
    cache = Cache(capacity=2, ttl=1, clock=clock)
    cache.store("key1", "value1")
    clock.advance(1)  # advance time to expire key1
    cache.store("key2", "value2")  # should reclaim stale key1
    assert cache.retrieve("key2") == "value2"  # key2 should be present

def test_removing_live_key():
    cache = Cache()
    cache.store("key1", "value1")
    assert cache.remove("key1") is True  # should succeed in removing
    assert cache.retrieve("key1") is None  # should be absent after removal

def test_removing_absent_key():
    cache = Cache()
    assert cache.remove("absent_key") is False  # should fail to remove absent key

def test_removing_stale_key():
    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)
    cache.store("key1", "value1")
    clock.advance(1)  # advance time to expire key1
    assert cache.remove("key1") is False  # should fail to remove stale key

def test_removing_stale_key_at_expiry_boundary():
    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)
    cache.store("key1", "value1")
    clock.advance(1)  # advance time to the expiry boundary
    assert cache.remove("key1") is False  # should fail to remove stale key

def test_cache_clear():
    cache = Cache()
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.clear()  # clear the cache
    assert cache.retrieve("key1") is None  # should be absent after clearing
    assert cache.retrieve("key2") is None  # should be absent after clearing

def test_stale_entries_absence_in_count_and_membership():
    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    clock.advance(1)  # advance time to expire key1
    assert cache.count() == 1  # only key2 should count
    assert not cache.contains("key1")  # key1 should be absent
    assert cache.contains("key2")  # key2 should be present

# Helper class to simulate a clock for testing
class FakeClock:
    def __init__(self):
        self.time = 0

    def advance(self, seconds):
        self.time += seconds

    def now(self):
        return self.time