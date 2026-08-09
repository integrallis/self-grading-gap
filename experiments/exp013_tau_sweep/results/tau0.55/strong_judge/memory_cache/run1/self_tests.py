import pytest

from solution import InMemoryCache

class FakeClock:
    def __init__(self):
        self.current_time = 0

    def advance(self, seconds):
        self.current_time += seconds

    def now(self):
        return self.current_time

def test_default_capacity_and_ttl():
    clock = FakeClock()
    cache = InMemoryCache(clock=clock)
    # Insert 100 distinct keys using default capacity
    for i in range(100):
        cache.set(f"key{i}", f"value{i}")
    # Inserting the 101st key should evict the least recently used entry
    cache.set("key100", "value100")
    # key0 is the least recently used and should be evicted
    assert cache.get("key0") is None

def test_default_ttl():
    clock = FakeClock()
    cache = InMemoryCache(clock=clock)
    cache.set("key1", "value1")
    clock.advance(59.9)  # Advance time to just before expiry
    assert cache.get("key1") == "value1"  # Should still be live
    clock.advance(0.1)  # Move to expiry
    assert cache.get("key1") is None  # Should be stale now

def test_configurable_capacity_and_ttl():
    clock = FakeClock()
    cache = InMemoryCache(capacity=50, ttl=30, clock=clock)
    assert cache is not None  # Just ensuring it can be created

def test_reject_capacity_below_one():
    with pytest.raises(Exception) as excinfo:
        InMemoryCache(capacity=0, clock=FakeClock())
    assert str(excinfo.value) == "capacity must be at least 1, got [0]"

    with pytest.raises(Exception) as excinfo:
        InMemoryCache(capacity=-5, clock=FakeClock())
    assert str(excinfo.value) == "capacity must be at least 1, got [-5]"

def test_reject_zero_or_negative_ttl():
    with pytest.raises(Exception) as excinfo:
        InMemoryCache(ttl=0, clock=FakeClock())
    assert str(excinfo.value) == "ttl must be positive, got [0]"

    with pytest.raises(Exception) as excinfo:
        InMemoryCache(ttl=-1, clock=FakeClock())
    assert str(excinfo.value) == "ttl must be positive, got [-1]"

def test_accept_positive_ttl():
    cache = InMemoryCache(ttl=1, clock=FakeClock())  # Acceptable value

def test_accept_fractional_positive_ttl():
    cache = InMemoryCache(ttl=0.5, clock=FakeClock())  # Acceptable value

def test_store_and_retrieve_value():
    clock = FakeClock()
    cache = InMemoryCache(clock=clock)
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"  # Stored value retrieved by key

def test_read_absent_key_without_fallback():
    clock = FakeClock()
    cache = InMemoryCache(clock=clock)
    assert cache.get("absent_key") is None  # Absent key yields nothing by default

def test_read_absent_key_with_fallback():
    clock = FakeClock()
    cache = InMemoryCache(clock=clock)
    assert cache.get("absent_key", "fallback_value") == "fallback_value"  # Fallback value returned

def test_replace_value_for_existing_key():
    clock = FakeClock()
    cache = InMemoryCache(clock=clock)
    cache.set("key1", "value1")
    cache.set("key1", "value2")  # Writing to an existing key replaces its value
    assert cache.get("key1") == "value2"

def test_replacement_does_not_increase_count():
    clock = FakeClock()
    cache = InMemoryCache(clock=clock)
    cache.set("key1", "value1")
    initial_count = cache.count()  # Assuming count method is available
    cache.set("key1", "value2")
    assert cache.count() == initial_count  # Count should remain unchanged

def test_eviction_when_cache_is_full():
    clock = FakeClock()
    cache = InMemoryCache(capacity=2, clock=clock)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")  # key1 should be evicted
    assert cache.get("key1") is None  # key1 evicted
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"

def test_reading_key_refreshes_recency():
    clock = FakeClock()
    cache = InMemoryCache(capacity=2, clock=clock)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.get("key1")  # Refresh recency of key1
    cache.set("key3", "value3")  # key2 should be evicted
    assert cache.get("key2") is None  # key2 evicted
    assert cache.get("key1") == "value1"
    assert cache.get("key3") == "value3"

def test_rewriting_key_refreshes_ttl():
    clock = FakeClock()
    cache = InMemoryCache(ttl=1, clock=clock)
    cache.set("key1", "value1")
    clock.advance(0.5)  # Wait for less than ttl
    cache.set("key1", "value2")  # Rewrite resets the ttl
    clock.advance(0.5)  # Wait for ttl to expire
    assert cache.get("key1") == "value2"  # key1 still valid after rewrite

def test_key_expires_after_ttl():
    clock = FakeClock()
    cache = InMemoryCache(ttl=1, clock=clock)
    cache.set("key1", "value1")
    clock.advance(1)  # Advance time to expire
    assert cache.get("key1") is None  # key1 should be stale

def test_key_is_stale_exactly_at_expiry_boundary():
    clock = FakeClock()
    cache = InMemoryCache(ttl=1, clock=clock)
    cache.set("key1", "value1")
    clock.advance(1)  # Advance time to expiry boundary
    assert cache.get("key1") is None  # key1 should be stale

def test_sweep_function_removes_stale_entries():
    clock = FakeClock()
    cache = InMemoryCache(ttl=1, clock=clock)
    cache.set("key1", "value1")
    clock.advance(1)  # Advance time to expire
    removed_count = cache.sweep()  # Sweep should remove stale entries
    assert removed_count == 1  # One stale entry removed
    assert cache.get("key1") is None  # key1 should be gone

def test_sweep_removes_multiple_stale_entries():
    clock = FakeClock()
    cache = InMemoryCache(ttl=1, clock=clock)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    clock.advance(1)  # Advance time to expire
    removed_count = cache.sweep()  # Sweep should remove stale entries
    assert removed_count == 2  # Two stale entries removed
    assert cache.get("key1") is None  # key1 should be gone
    assert cache.get("key2") is None  # key2 should be gone

def test_cache_count_respects_staleness():
    clock = FakeClock()
    cache = InMemoryCache(ttl=1, clock=clock)
    cache.set("key1", "value1")
    assert cache.count() == 1  # Count should reflect one entry
    clock.advance(1)  # Advance time to expire
    assert cache.count() == 0  # Count should reflect zero entries

def test_remove_live_key():
    clock = FakeClock()
    cache = InMemoryCache(clock=clock)
    cache.set("key1", "value1")
    assert cache.remove("key1") is True  # Removing a live key should succeed
    assert cache.get("key1") is None  # key1 should be absent

def test_remove_absent_key():
    clock = FakeClock()
    cache = InMemoryCache(clock=clock)
    assert cache.remove("absent_key") is False  # Removing an absent key should fail

def test_remove_key_at_expiry_boundary():
    clock = FakeClock()
    cache = InMemoryCache(ttl=1, clock=clock)
    cache.set("key1", "value1")
    clock.advance(1)  # Advance time to expiry boundary
    assert cache.remove("key1") is False  # Removing key exactly at expiry boundary should fail

def test_clear_cache_leaves_no_entries():
    clock = FakeClock()
    cache = InMemoryCache(clock=clock)
    cache.set("key1", "value1")
    cache.clear()  # Clear should empty the cache
    assert cache.count() == 0  # Cache should have no entries

def test_eviction_reclaims_stale_slot_before_live_entry():
    clock = FakeClock()
    cache = InMemoryCache(capacity=2, ttl=1, clock=clock)
    cache.set("key1", "value1")
    clock.advance(1)  # Advance time to expire key1
    cache.set("key2", "value2")  # key1 is stale, should reclaim its slot
    assert cache.get("key1") is None  # key1 should be gone
    assert cache.get("key2") == "value2"  # key2 should still be there

def test_rewrite_stale_key():
    clock = FakeClock()
    cache = InMemoryCache(ttl=1, clock=clock)
    cache.set("key1", "value1")
    clock.advance(1)  # Advance time to expire key1
    cache.set("key1", "value2")  # Rewrite with a fresh value
    assert cache.get("key1") == "value2"  # Should retrieve the new value
    clock.advance(0.5)  # Advance time for the new TTL
    assert cache.get("key1") == "value2"  # Should still be valid