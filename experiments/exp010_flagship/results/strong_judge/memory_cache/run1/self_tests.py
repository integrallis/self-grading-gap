import pytest

from solution import Cache

class FakeClock:
    def __init__(self):
        self.current_time = 0

    def advance(self, seconds):
        self.current_time += seconds
        return self.current_time

def test_default_configuration():
    clock = FakeClock()
    cache = Cache(clock)
    assert cache.capacity == 100  # AC-1.1
    assert cache.time_to_live == 60  # AC-1.1

def test_configurable_capacity_and_ttl():
    clock = FakeClock()
    cache = Cache(clock, capacity=50, time_to_live=30)
    assert cache.capacity == 50  # AC-1.2
    assert cache.time_to_live == 30  # AC-1.2

def test_capacity_below_one_rejected():
    clock = FakeClock()
    with pytest.raises(ValueError) as excinfo:
        Cache(clock, capacity=0)
    assert str(excinfo.value) == "capacity must be at least 1, got [0]"  # AC-1.3
    
    with pytest.raises(ValueError) as excinfo:
        Cache(clock, capacity=-5)
    assert str(excinfo.value) == "capacity must be at least 1, got [-5]"  # AC-1.3

def test_ttl_zero_or_negative_rejected():
    clock = FakeClock()
    with pytest.raises(ValueError) as excinfo:
        Cache(clock, time_to_live=0)
    assert str(excinfo.value) == "ttl must be positive, got [0]"  # AC-1.4

    with pytest.raises(ValueError) as excinfo:
        Cache(clock, time_to_live=-1)
    assert str(excinfo.value) == "ttl must be positive, got [-1]"  # AC-1.4

def test_positive_ttl_accepted():
    clock = FakeClock()
    cache = Cache(clock, time_to_live=1.0)  # AC-1.5
    assert cache.time_to_live == 1.0  # AC-1.5
    cache = Cache(clock, time_to_live=0.5)  # AC-1.5
    assert cache.time_to_live == 0.5  # AC-1.5

def test_store_and_retrieve_value():
    clock = FakeClock()
    cache = Cache(clock)
    cache.store("key1", "value1")
    assert cache.retrieve("key1") == "value1"  # AC-2.1

def test_retrieve_absent_key():
    clock = FakeClock()
    cache = Cache(clock)
    assert cache.retrieve("absent_key") is None  # AC-2.2
    assert cache.retrieve("absent_key", "default") == "default"  # AC-2.2

def test_store_existing_key_replaces_value():
    clock = FakeClock()
    cache = Cache(clock)
    cache.store("key1", "value1")
    cache.store("key1", "value2")
    assert cache.retrieve("key1") == "value2"  # AC-2.3
    assert cache.count() == 1  # Check count remains unchanged

def test_lru_eviction():
    clock = FakeClock()
    cache = Cache(clock, capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key3", "value3")  # Evicts "key1"
    assert cache.retrieve("key1") is None  # AC-3.1
    assert cache.retrieve("key2") == "value2"  # AC-3.1
    assert cache.retrieve("key3") == "value3"  # AC-3.1

def test_reading_key_refreshes_recency():
    clock = FakeClock()
    cache = Cache(clock, capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.retrieve("key1")  # Refresh "key1"
    cache.store("key3", "value3")  # Evicts "key2"
    assert cache.retrieve("key2") is None  # AC-3.2
    assert cache.retrieve("key1") == "value1"  # AC-3.2
    assert cache.retrieve("key3") == "value3"  # AC-3.2

def test_rewriting_key_refreshes_recency():
    clock = FakeClock()
    cache = Cache(clock, capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key1", "value1_updated")  # Refresh "key1"
    cache.store("key3", "value3")  # Evicts "key2"
    assert cache.retrieve("key2") is None  # AC-3.3
    assert cache.retrieve("key1") == "value1_updated"  # AC-3.3
    assert cache.retrieve("key3") == "value3"  # AC-3.3

def test_capacity_one_evicts_previous_entry():
    clock = FakeClock()
    cache = Cache(clock, capacity=1)
    cache.store("key1", "value1")
    cache.store("key2", "value2")  # Evicts "key1"
    assert cache.retrieve("key1") is None  # AC-3.4
    assert cache.retrieve("key2") == "value2"  # AC-3.4

def test_entry_expires_after_ttl():
    clock = FakeClock()
    cache = Cache(clock, time_to_live=1)  # 1 second TTL
    cache.store("key1", "value1")
    clock.advance(1)  # Move to expiry
    assert cache.retrieve("key1") is None  # AC-4.1

def test_entry_is_still_served_before_expiry():
    clock = FakeClock()
    cache = Cache(clock, time_to_live=1)  # 1 second TTL
    cache.store("key1", "value1")
    assert cache.retrieve("key1") == "value1"  # AC-4.2
    clock.advance(0.5)
    assert cache.retrieve("key1") == "value1"  # AC-4.2

def test_rewriting_key_restores_ttl():
    clock = FakeClock()
    cache = Cache(clock, time_to_live=1)  # 1 second TTL
    cache.store("key1", "value1")
    clock.advance(0.5)
    cache.store("key1", "value1_updated")  # Refresh TTL
    clock.advance(0.5)  # Now at t=1.0, key1 should still be valid
    assert cache.retrieve("key1") == "value1_updated"  # AC-4.3
    clock.advance(0.1)  # Move to expiry
    assert cache.retrieve("key1") is None  # AC-4.3

def test_stale_key_accepts_fresh_value():
    clock = FakeClock()
    cache = Cache(clock, time_to_live=1)  # 1 second TTL
    cache.store("key1", "value1")
    clock.advance(1)  # Wait for expiration
    cache.store("key1", "value1_fresh")  # Accept fresh value
    assert cache.retrieve("key1") == "value1_fresh"  # AC-4.4

def test_entry_count_treats_stale_entries_as_absent():
    clock = FakeClock()
    cache = Cache(clock, capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    clock.advance(1)  # Move to expiry
    assert cache.count() == 0  # AC-5.1

def test_explicit_sweep_removes_stale_entries():
    clock = FakeClock()
    cache = Cache(clock, capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    clock.advance(1)  # Move to expiry
    removed_count = cache.sweep()  # AC-5.2
    assert removed_count == 2  # AC-5.2
    assert cache.count() == 0  # AC-5.2

def test_full_cache_reclaims_stale_slots_first():
    clock = FakeClock()
    cache = Cache(clock, capacity=2, time_to_live=1)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    clock.advance(1)  # Move to expiry
    cache.store("key3", "value3")  # Should reclaim stale key1
    assert cache.retrieve("key1") is None  # AC-5.3
    assert cache.retrieve("key2") is None  # AC-5.3
    assert cache.retrieve("key3") == "value3"  # AC-5.3

def test_remove_live_key_reports_success():
    clock = FakeClock()
    cache = Cache(clock)
    cache.store("key1", "value1")
    assert cache.remove("key1") is True  # AC-5.4
    assert cache.retrieve("key1") is None  # AC-5.4

def test_remove_absent_key_reports_failure():
    clock = FakeClock()
    cache = Cache(clock)
    assert cache.remove("absent_key") is False  # AC-5.5

def test_remove_key_exactly_at_expiry_boundary_reports_failure():
    clock = FakeClock()
    cache = Cache(clock, time_to_live=1)
    cache.store("key1", "value1")
    clock.advance(1)  # Move to expiry
    assert cache.remove("key1") is False  # AC-5.5

def test_clear_cache_leaves_it_empty():
    clock = FakeClock()
    cache = Cache(clock)
    cache.store("key1", "value1")
    cache.clear()  # AC-5.6
    assert cache.count() == 0  # AC-5.6

def test_membership_checks():
    clock = FakeClock()
    cache = Cache(clock, time_to_live=1)
    cache.store("key1", "value1")
    assert cache.has("key1") is True  # Check live key
    clock.advance(1)  # Move to expiry
    assert cache.has("key1") is False  # Check stale key