import pytest
import time

from solution import Cache

def test_default_configuration():
    cache = Cache()
    assert cache.capacity == 100  # AC-1.1
    assert cache.ttl == 60  # AC-1.1

def test_configured_capacity_and_ttl():
    cache = Cache(capacity=50, ttl=30)
    assert cache.capacity == 50  # AC-1.2
    assert cache.ttl == 30  # AC-1.2

def test_capacity_below_one_rejected():
    # Testing for capacity below 1
    with pytest.raises(Exception, match=r"^capacity must be at least 1, got \[0\]$"):
        Cache(capacity=0)  # AC-1.3
    with pytest.raises(Exception, match=r"^capacity must be at least 1, got \[-1\]$"):
        Cache(capacity=-1)  # AC-1.3
    with pytest.raises(Exception, match=r"^capacity must be at least 1, got \[-0.5\]$"):
        Cache(capacity=-0.5)  # AC-1.3
    with pytest.raises(Exception, match=r"^capacity must be at least 1, got \[0.5\]$"):
        Cache(capacity=0.5)  # AC-1.3

def test_ttl_zero_or_negative_rejected():
    # Testing for zero or negative TTL
    with pytest.raises(Exception, match=r"^ttl must be positive, got \[0\]$"):
        Cache(ttl=0)  # AC-1.4
    with pytest.raises(Exception, match=r"^ttl must be positive, got \[-1.5\]$"):
        Cache(ttl=-1.5)  # AC-1.4

def test_positive_ttl_accepted():
    cache = Cache(ttl=0.5)  # AC-1.5
    assert cache.ttl == 0.5  # AC-1.5
    cache = Cache(ttl=60.5)  # AC-1.5
    assert cache.ttl == 60.5  # AC-1.5

def test_store_and_retrieve():
    cache = Cache()
    cache.store("key1", "value1")
    assert cache.retrieve("key1") == "value1"  # AC-2.1

def test_retrieve_absent_key():
    cache = Cache()
    assert cache.retrieve("absent_key") is None  # AC-2.2
    assert cache.retrieve("absent_key", fallback="fallback_value") == "fallback_value"  # AC-2.2

def test_store_existing_key_replaces_value():
    cache = Cache()
    cache.store("key1", "value1")
    cache.store("key1", "value2")
    assert cache.retrieve("key1") == "value2"  # AC-2.3

def test_store_existing_key_does_not_increase_count():
    cache = Cache()
    cache.store("key1", "value1")
    initial_count = cache.count()
    cache.store("key1", "value2")
    assert cache.count() == initial_count  # AC-2.3

def test_eviction_when_full():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key3", "value3")  # This should evict "key1"
    assert cache.retrieve("key1") is None  # AC-3.1
    assert cache.retrieve("key2") == "value2"  # AC-3.1
    assert cache.retrieve("key3") == "value3"  # AC-3.1

def test_reading_key_refreshes_recency():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.retrieve("key1")  # Refresh recency for key1
    cache.store("key3", "value3")  # This should evict "key2"
    assert cache.retrieve("key2") is None  # AC-3.2
    assert cache.retrieve("key1") == "value1"  # AC-3.2

def test_rewriting_existing_key_refreshes_recency():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key1", "value1_updated")  # Refresh recency for key1
    cache.store("key3", "value3")  # This should evict "key2"
    assert cache.retrieve("key2") is None  # AC-3.3
    assert cache.retrieve("key1") == "value1_updated"  # AC-3.3

def test_cache_with_capacity_one():
    cache = Cache(capacity=1)
    cache.store("key1", "value1")
    cache.store("key2", "value2")  # Should replace key1
    assert cache.retrieve("key1") is None  # AC-3.4
    assert cache.retrieve("key2") == "value2"  # AC-3.4

def test_entry_expiry():
    clock = lambda: time.time() + 1  # Control time for testing
    cache = Cache(ttl=1)
    cache.store("key1", "value1")
    assert cache.retrieve("key1") == "value1"  # Before expiry
    time.sleep(1)  # Wait for expiry
    assert cache.retrieve("key1") is None  # AC-4.1

def test_entry_still_served_before_expiry():
    clock = lambda: time.time() + 0.5  # Control time for testing
    cache = Cache(ttl=1)
    cache.store("key1", "value1")
    assert cache.retrieve("key1") == "value1"  # AC-4.2

def test_rewriting_key_resets_ttl():
    clock = lambda: time.time() + 0.5  # Control time for testing
    cache = Cache(ttl=1)
    cache.store("key1", "value1")
    time.sleep(0.5)
    cache.store("key1", "value1_updated")  # Reset ttl
    assert cache.retrieve("key1") == "value1_updated"  # AC-4.3
    time.sleep(0.5)  # Wait for expiry
    assert cache.retrieve("key1") is None  # AC-4.1

def test_expired_key_accepts_fresh_value():
    clock = lambda: time.time() + 1  # Control time for testing
    cache = Cache(ttl=1)
    cache.store("key1", "value1")
    time.sleep(1)
    cache.store("key1", "value1_fresh")  # Should accept fresh value
    assert cache.retrieve("key1") == "value1_fresh"  # AC-4.4

def test_counting_stale_entries():
    clock = lambda: time.time() + 1  # Control time for testing
    cache = Cache(ttl=1)
    cache.store("key1", "value1")
    time.sleep(1)
    assert cache.count() == 0  # AC-5.1

def test_sweep_removes_stale_entries():
    clock = lambda: time.time() + 1  # Control time for testing
    cache = Cache(ttl=1)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    time.sleep(1)
    removed_count = cache.sweep()  # AC-5.2
    assert removed_count == 2  # AC-5.2
    assert cache.count() == 0  # AC-5.2

def test_full_cache_reclaims_stale_slots():
    clock = lambda: time.time() + 1  # Control time for testing
    cache = Cache(capacity=2, ttl=1)
    cache.store("key1", "value1")
    time.sleep(1)  # key1 is now stale
    cache.store("key2", "value2")  # Should reclaim stale key1
    cache.store("key3", "value3")  # key2 should be evicted
    assert cache.retrieve("key1") is None  # AC-5.3
    assert cache.retrieve("key2") == "value2"  # AC-5.3
    assert cache.retrieve("key3") == "value3"  # AC-5.3

def test_remove_live_key():
    cache = Cache()
    cache.store("key1", "value1")
    assert cache.remove("key1") == True  # AC-5.4
    assert cache.retrieve("key1") is None  # AC-5.4

def test_remove_absent_key():
    cache = Cache()
    assert cache.remove("absent_key") == False  # AC-5.5

def test_remove_key_at_expiry_boundary():
    clock = lambda: time.time() + 1  # Control time for testing
    cache = Cache(ttl=1)
    cache.store("key1", "value1")
    time.sleep(1)  # key1 is now stale
    assert cache.remove("key1") == False  # AC-5.5

def test_clear_cache():
    cache = Cache()
    cache.store("key1", "value1")
    cache.clear()  # AC-5.6
    assert cache.count() == 0  # AC-5.6