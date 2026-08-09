import pytest
from solution import Cache

# US-1: Configuration
def test_default_capacity_and_ttl():
    cache = Cache(lambda: 0)  # Providing a clock
    assert cache.capacity == 100  # AC-1.1
    assert cache.ttl == 60  # AC-1.1

def test_custom_capacity_and_ttl():
    cache = Cache(lambda: 0, capacity=50, ttl=30)
    assert cache.capacity == 50  # AC-1.2
    assert cache.ttl == 30  # AC-1.2

def test_capacity_below_one_rejected():
    with pytest.raises(ValueError, match=r"^capacity must be at least 1, got \[0\]$"):
        Cache(lambda: 0, capacity=0)  # AC-1.3
    with pytest.raises(ValueError, match=r"^capacity must be at least 1, got \[-1\]$"):
        Cache(lambda: 0, capacity=-1)  # AC-1.3

def test_zero_or_negative_ttl_rejected():
    with pytest.raises(ValueError, match=r"^ttl must be positive, got \[0\]$"):
        Cache(lambda: 0, ttl=0)  # AC-1.4
    with pytest.raises(ValueError, match=r"^ttl must be positive, got \[-1\]$"):
        Cache(lambda: 0, ttl=-1)  # AC-1.4

def test_positive_ttl_accepted():
    cache = Cache(lambda: 0, ttl=1)
    assert cache.ttl == 1  # AC-1.5
    cache = Cache(lambda: 0, ttl=0.5)
    assert cache.ttl == 0.5  # AC-1.5

# US-2: Store and retrieve
def test_store_and_retrieve_value():
    cache = Cache(lambda: 0)
    cache.store("key1", "value1")
    assert cache.retrieve("key1") == "value1"  # AC-2.1

def test_retrieve_absent_key():
    cache = Cache(lambda: 0)
    assert cache.retrieve("absent_key") is None  # AC-2.2
    assert cache.retrieve("absent_key", "fallback_value") == "fallback_value"  # AC-2.2

def test_rewrite_existing_key():
    cache = Cache(lambda: 0)
    cache.store("key1", "value1")
    cache.store("key1", "value2")
    assert cache.retrieve("key1") == "value2"  # AC-2.3
    assert cache.count() == 1  # Ensure count does not increase

# US-3: Least-recently-used eviction
def test_insert_into_full_cache_evicts_lru():
    cache = Cache(lambda: 0, capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key3", "value3")  # This should evict key1
    assert cache.retrieve("key1") is None  # AC-3.1
    assert cache.retrieve("key2") == "value2"  # AC-3.1
    assert cache.retrieve("key3") == "value3"  # AC-3.1

def test_reading_key_refreshes_recency():
    cache = Cache(lambda: 0, capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.retrieve("key1")  # Refresh recency of key1
    cache.store("key3", "value3")  # This should evict key2
    assert cache.retrieve("key2") is None  # AC-3.2
    assert cache.retrieve("key1") == "value1"  # AC-3.2
    assert cache.retrieve("key3") == "value3"  # AC-3.2

def test_rewriting_existing_key_refreshes_recency():
    cache = Cache(lambda: 0, capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key1", "value1_new")  # Refresh recency of key1
    cache.store("key3", "value3")  # This should evict key2
    assert cache.retrieve("key2") is None  # AC-3.3
    assert cache.retrieve("key1") == "value1_new"  # AC-3.3
    assert cache.retrieve("key3") == "value3"  # AC-3.3

def test_capacity_of_one_eviction():
    cache = Cache(lambda: 0, capacity=1)
    cache.store("key1", "value1")
    cache.store("key2", "value2")  # This should evict key1
    assert cache.retrieve("key1") is None  # AC-3.4
    assert cache.retrieve("key2") == "value2"  # AC-3.4

# US-4: Expiry
def test_entry_expiry():
    now = [0]
    cache = Cache(lambda: now[0], ttl=1)
    cache.store("key1", "value1")
    now[0] = 1  # Simulating time passing
    assert cache.retrieve("key1") is None  # AC-4.1

def test_entry_served_before_expiry():
    now = [0]
    cache = Cache(lambda: now[0], ttl=60)
    cache.store("key1", "value1")
    now[0] = 59  # Before expiry
    assert cache.retrieve("key1") == "value1"  # AC-4.2

def test_rewriting_key_resets_ttl():
    now = [0]
    cache = Cache(lambda: now[0], ttl=60)
    cache.store("key1", "value1")
    now[0] = 30
    cache.store("key1", "value1_new")  # Reset ttl
    now[0] = 90  # Now it should expire
    assert cache.retrieve("key1") is None  # AC-4.3

def test_stale_key_accepts_fresh_value():
    now = [0]
    cache = Cache(lambda: now[0], ttl=1)
    cache.store("key1", "value1")
    now[0] = 1  # Simulating time passing
    assert cache.retrieve("key1") is None  # Should be stale
    cache.store("key1", "value1_fresh")  # Accept fresh value
    assert cache.retrieve("key1") == "value1_fresh"  # AC-4.4

# US-5: Housekeeping
def test_count_and_membership_check_stale_entries():
    now = [0]
    cache = Cache(lambda: now[0], capacity=2, ttl=1)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    now[0] = 1  # Simulating time passing
    assert cache.count() == 0  # AC-5.1
    assert not cache.contains("key1")  # AC-5.1
    assert not cache.contains("key2")  # AC-5.1

def test_sweep_removes_stale_entries():
    now = [0]
    cache = Cache(lambda: now[0], capacity=2, ttl=1)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    now[0] = 1  # Simulating time passing
    removed_count = cache.sweep()  # Should remove both entries
    assert removed_count == 2  # AC-5.2
    assert cache.count() == 0  # AC-5.2

def test_full_cache_reclaims_stale_slots():
    now = [0]
    cache = Cache(lambda: now[0], capacity=2, ttl=1)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    now[0] = 1  # Simulating time passing
    cache.store("key3", "value3")  # Should reclaim stale key1
    assert cache.retrieve("key1") is None  # AC-5.3
    assert cache.retrieve("key2") is None  # AC-5.3
    assert cache.retrieve("key3") == "value3"  # AC-5.3

def test_remove_live_key():
    cache = Cache(lambda: 0)
    cache.store("key1", "value1")
    assert cache.remove("key1") is True  # AC-5.4
    assert cache.retrieve("key1") is None  # AC-5.4

def test_remove_absent_key():
    cache = Cache(lambda: 0)
    assert cache.remove("absent_key") is False  # AC-5.5

def test_remove_key_at_expiry_boundary():
    now = [0]
    cache = Cache(lambda: now[0], ttl=1)
    cache.store("key1", "value1")
    now[0] = 1  # Simulating time passing
    assert cache.remove("key1") is False  # AC-5.5

def test_clear_cache():
    cache = Cache(lambda: 0)
    cache.store("key1", "value1")
    cache.clear()
    assert cache.count() == 0  # AC-5.6