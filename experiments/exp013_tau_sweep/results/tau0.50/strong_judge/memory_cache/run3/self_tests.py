import pytest

from solution import Cache

def test_default_capacity_and_ttl():
    cache = Cache()
    assert cache.capacity == 100  # AC-1.1
    assert cache.ttl == 60  # AC-1.1

def test_configured_capacity_and_ttl():
    cache = Cache(capacity=50, ttl=30)
    assert cache.capacity == 50  # AC-1.2
    assert cache.ttl == 30  # AC-1.2

def test_invalid_capacity_below_one():
    with pytest.raises(Exception) as excinfo:
        Cache(capacity=0)  # AC-1.3
    assert str(excinfo.value) == "capacity must be at least 1, got [0]"

    with pytest.raises(Exception) as excinfo:
        Cache(capacity=-1)  # AC-1.3
    assert str(excinfo.value) == "capacity must be at least 1, got [-1]"

def test_invalid_ttl_zero_or_negative():
    with pytest.raises(Exception) as excinfo:
        Cache(ttl=0)  # AC-1.4
    assert str(excinfo.value) == "ttl must be positive, got [0]"

    with pytest.raises(Exception) as excinfo:
        Cache(ttl=-1.5)  # AC-1.4
    assert str(excinfo.value) == "ttl must be positive, got [-1.5]"

def test_valid_ttl():
    cache = Cache(ttl=0.5)  # AC-1.5
    assert cache.ttl == 0.5  # AC-1.5

def test_store_and_retrieve_value():
    cache = Cache()
    cache.store("key1", "value1")
    assert cache.retrieve("key1") == "value1"  # AC-2.1

def test_retrieve_absent_key_without_fallback():
    cache = Cache()
    assert cache.retrieve("absent_key") is None  # AC-2.2

def test_retrieve_absent_key_with_fallback():
    cache = Cache()
    assert cache.retrieve("absent_key", fallback="default") == "default"  # AC-2.2

def test_store_overwrite_existing_key():
    cache = Cache()
    cache.store("key1", "value1")
    cache.store("key1", "value2")
    assert cache.retrieve("key1") == "value2"  # AC-2.3
    assert cache.count() == 1  # Ensure count unchanged after overwrite

def test_full_cache_eviction():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key3", "value3")  # Evicts "key1"
    assert cache.retrieve("key1") is None  # AC-3.1
    assert cache.retrieve("key2") == "value2"  # AC-3.1
    assert cache.retrieve("key3") == "value3"  # AC-3.1

def test_read_refreshes_recency():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.retrieve("key1")  # Refresh recency for key1
    cache.store("key3", "value3")  # Evicts "key2"
    assert cache.retrieve("key2") is None  # AC-3.2
    assert cache.retrieve("key1") == "value1"  # AC-3.2
    assert cache.retrieve("key3") == "value3"  # AC-3.2

def test_rewrite_key_refreshes_recency():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key1", "new_value1")  # Rewrite key1
    cache.store("key3", "value3")  # Insert new key to check eviction
    assert cache.retrieve("key1") == "new_value1"  # AC-3.3
    assert cache.retrieve("key2") is None  # AC-3.3, key2 should be evicted
    assert cache.retrieve("key3") == "value3"  # AC-3.3

def test_capacity_one_replaces_previous_entry():
    cache = Cache(capacity=1)
    cache.store("key1", "value1")
    cache.store("key2", "value2")  # Replaces key1
    assert cache.retrieve("key1") is None  # AC-3.4
    assert cache.retrieve("key2") == "value2"  # AC-3.4

def test_entry_expiry_with_fake_clock():
    class FakeClock:
        def __init__(self):
            self.time = 0

        def advance(self, seconds):
            self.time += seconds
            return self.time

    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)  # Set TTL to 1 second
    cache.store("key1", "value1")
    clock.advance(1)  # Simulate time passing
    assert cache.retrieve("key1") is None  # AC-4.1

def test_entry_still_valid_before_expiry_with_fake_clock():
    class FakeClock:
        def __init__(self):
            self.time = 0

        def advance(self, seconds):
            self.time += seconds
            return self.time

    clock = FakeClock()
    cache = Cache(ttl=2, clock=clock)  # Set TTL to 2 seconds
    cache.store("key1", "value1")
    clock.advance(1)  # Simulate time passing
    assert cache.retrieve("key1") == "value1"  # AC-4.2

def test_rewrite_key_resets_ttl_with_fake_clock():
    class FakeClock:
        def __init__(self):
            self.time = 0

        def advance(self, seconds):
            self.time += seconds
            return self.time

    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)  # Set TTL to 1 second
    cache.store("key1", "value1")
    clock.advance(0.5)  # Simulate time passing
    cache.store("key1", "value2")  # Resets TTL
    clock.advance(0.5)  # Simulate more time passing
    assert cache.retrieve("key1") == "value2"  # AC-4.3
    clock.advance(0.5)  # Advance to TTL boundary
    assert cache.retrieve("key1") is None  # AC-4.3

def test_stale_entry_accepts_fresh_value_with_fake_clock():
    class FakeClock:
        def __init__(self):
            self.time = 0

        def advance(self, seconds):
            self.time += seconds
            return self.time

    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)  # Set TTL to 1 second
    cache.store("key1", "value1")
    clock.advance(1)  # Simulate time passing
    cache.store("key1", "new_value1")  # Accepts fresh value after stale
    assert cache.retrieve("key1") == "new_value1"  # AC-4.4

def test_entry_count_treats_stale_entries_as_absent_with_fake_clock():
    class FakeClock:
        def __init__(self):
            self.time = 0

        def advance(self, seconds):
            self.time += seconds
            return self.time

    clock = FakeClock()
    cache = Cache(capacity=2, ttl=1, clock=clock)
    cache.store("key1", "value1")
    assert cache.count() == 1  # AC-5.1
    clock.advance(1)  # Simulate time passing
    assert cache.count() == 0  # AC-5.1

def test_explicit_sweep_removes_stale_entries_with_fake_clock():
    class FakeClock:
        def __init__(self):
            self.time = 0

        def advance(self, seconds):
            self.time += seconds
            return self.time

    clock = FakeClock()
    cache = Cache(capacity=2, ttl=1, clock=clock)
    cache.store("key1", "value1")
    clock.advance(1)  # Simulate time passing
    assert cache.sweep() == 1  # AC-5.2
    assert cache.count() == 0  # AC-5.2

def test_full_cache_reclaims_stale_slots_before_eviction_with_fake_clock():
    class FakeClock:
        def __init__(self):
            self.time = 0

        def advance(self, seconds):
            self.time += seconds
            return self.time

    clock = FakeClock()
    cache = Cache(capacity=2, ttl=1, clock=clock)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    clock.advance(1)  # Make key1 stale
    cache.store("key3", "value3")  # Insert new key
    assert cache.retrieve("key1") is None  # AC-5.3
    assert cache.retrieve("key2") == "value2"  # AC-5.3
    assert cache.retrieve("key3") == "value3"  # AC-5.3

def test_remove_live_key_reports_success():
    cache = Cache()
    cache.store("key1", "value1")
    assert cache.remove("key1") is True  # AC-5.4
    assert cache.retrieve("key1") is None  # AC-5.4

def test_remove_absent_key_reports_failure():
    cache = Cache()
    assert cache.remove("absent_key") is False  # AC-5.5

def test_remove_key_at_expiry_boundary_reports_failure_with_fake_clock():
    class FakeClock:
        def __init__(self):
            self.time = 0

        def advance(self, seconds):
            self.time += seconds
            return self.time

    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)  # Set TTL to 1 second
    cache.store("key1", "value1")
    clock.advance(1)  # Simulate time passing
    assert cache.remove("key1") is False  # AC-5.5

def test_clear_cache_leaves_no_entries():
    cache = Cache()
    cache.store("key1", "value1")
    cache.clear()  # AC-5.6
    assert cache.count() == 0  # AC-5.6

def test_membership_check_for_live_and_stale_keys_with_fake_clock():
    class FakeClock:
        def __init__(self):
            self.time = 0

        def advance(self, seconds):
            self.time += seconds
            return self.time

    clock = FakeClock()
    cache = Cache(ttl=1, clock=clock)  # Set TTL to 1 second
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    assert cache.retrieve("key1") is not None  # Live key
    assert cache.retrieve("key2") is not None  # Live key
    clock.advance(1)  # Make entries stale
    assert cache.retrieve("key1") is None  # Stale key
    assert cache.retrieve("key2") is None  # Stale key