import pytest
from solution import Cache

def test_default_configuration():
    cache = Cache()
    assert cache.capacity == 100  # AC-1.1: Default capacity is 100 entries
    assert cache.ttl == 60  # AC-1.1: Default time-to-live is 60 seconds

def test_configurable_capacity_and_ttl():
    cache = Cache(capacity=50, ttl=30)
    assert cache.capacity == 50  # AC-1.2: Capacity can be set to 50
    assert cache.ttl == 30  # AC-1.2: TTL can be set to 30 seconds

def test_capacity_below_one_rejected():
    with pytest.raises(Exception, match=r"^capacity must be at least 1, got \[-1\]$"):
        Cache(capacity=-1)  # AC-1.3: Capacity below 1 should raise error
    with pytest.raises(Exception, match=r"^capacity must be at least 1, got \[0\]$"):
        Cache(capacity=0)  # AC-1.3: Capacity 0 should raise error

def test_zero_or_negative_ttl_rejected():
    with pytest.raises(Exception, match=r"^ttl must be positive, got \[-1\]$"):
        Cache(ttl=-1)  # AC-1.4: Negative TTL should raise error
    with pytest.raises(Exception, match=r"^ttl must be positive, got \[0\]$"):
        Cache(ttl=0)  # AC-1.4: Zero TTL should raise error

def test_positive_ttl_accepted():
    cache = Cache(ttl=1)  
    assert cache.ttl == 1  # AC-1.5: TTL of 1 second is accepted
    cache = Cache(ttl=2.5)  
    assert cache.ttl == 2.5  # AC-1.5: TTL of 2.5 seconds is accepted
    cache = Cache(ttl=0.5)  
    assert cache.ttl == 0.5  # AC-1.5: Sub-second TTL is accepted

def test_store_and_retrieve_value():
    cache = Cache()
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"  # AC-2.1: Retrieve stored value

def test_retrieve_absent_key():
    cache = Cache()
    assert cache.get("absent_key") is None  # AC-2.2: Absent key yields None
    assert cache.get("absent_key", "fallback") == "fallback"  # AC-2.2: Absent key with fallback

def test_rewrite_existing_key():
    cache = Cache()
    cache.set("key1", "value1")
    cache.set("key1", "value2")
    assert cache.get("key1") == "value2"  # AC-2.3: Rewrite existing key updates value
    assert cache.count() == 1  # AC-2.3: Count remains unchanged

def test_lru_eviction():
    cache = Cache(capacity=2)  # Set capacity to 2
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")  # This should evict key1
    assert cache.get("key1") is None  # AC-3.1: key1 should be evicted
    assert cache.get("key2") == "value2"  # AC-3.1: key2 remains
    assert cache.get("key3") == "value3"  # AC-3.1: key3 remains

def test_read_refreshes_recency():
    cache = Cache(capacity=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.get("key1")  # Access key1 to refresh its recency
    cache.set("key3", "value3")  # key2 should be evicted
    assert cache.get("key2") is None  # AC-3.2: key2 should be evicted
    assert cache.get("key1") == "value1"  # AC-3.2: key1 remains
    assert cache.get("key3") == "value3"  # AC-3.2: key3 remains

def test_rewrite_key_refreshes_recency():
    cache = Cache(capacity=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key1", "value1_updated")  # Rewrite key1
    cache.set("key3", "value3")  # This should evict key2
    assert cache.get("key2") is None  # AC-3.3: key2 should be evicted
    assert cache.get("key1") == "value1_updated"  # AC-3.3: key1 should be updated

def test_capacity_one_replaces_previous():
    cache = Cache(capacity=1)  # Set capacity to 1
    cache.set("key1", "value1")
    cache.set("key2", "value2")  # This should replace key1
    assert cache.get("key1") is None  # AC-3.4: key1 should be evicted
    assert cache.get("key2") == "value2"  # AC-3.4: key2 remains

def test_entry_expiry(clock):
    cache = Cache(ttl=2, clock=clock)  # Set TTL to 2 seconds
    cache.set("key1", "value1")
    clock.sleep(2)  # Wait for expiry
    assert cache.get("key1") is None  # AC-4.1: key1 should be stale

def test_entry_still_served_before_expiry(clock):
    cache = Cache(ttl=2, clock=clock)
    cache.set("key1", "value1")
    clock.sleep(1)  # Wait for 1 second
    assert cache.get("key1") == "value1"  # AC-4.2: key1 should still be served

def test_rewrite_key_restarts_ttl(clock):
    cache = Cache(ttl=2, clock=clock)
    cache.set("key1", "value1")
    clock.sleep(1)  # Wait for 1 second
    cache.set("key1", "value1_updated")  # Rewrite key1
    clock.sleep(1)  # Wait for another second
    assert cache.get("key1") == "value1_updated"  # AC-4.3: key1 should not be stale

def test_expired_key_accepts_fresh_value(clock):
    cache = Cache(ttl=2, clock=clock)
    cache.set("key1", "value1")
    clock.sleep(2)
    cache.set("key1", "value1_fresh")  # Adding fresh value after expiry
    assert cache.get("key1") == "value1_fresh"  # AC-4.4: key1 should now return fresh value

def test_count_and_membership_checks_treat_stale_entries_as_absent(clock):
    cache = Cache(ttl=2, clock=clock)
    cache.set("key1", "value1")
    assert cache.count() == 1  # AC-5.1: Count should be 1 before expiry
    clock.sleep(2)
    assert cache.count() == 0  # AC-5.1: Count should be 0 after expiry
    assert "key1" not in cache  # AC-5.1: Stale key1 should be absent

def test_explicit_sweep_removes_stale_entries(clock):
    cache = Cache(ttl=2, clock=clock)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    clock.sleep(2)
    removed_count = cache.sweep()  # Sweep to remove stale entries
    assert removed_count == 2  # AC-5.2: Two stale entries should be removed
    assert cache.count() == 0  # AC-5.2: Count should be 0 after sweep

def test_full_cache_reclaims_stale_slots_first(clock):
    cache = Cache(capacity=2, ttl=2, clock=clock)
    cache.set("key1", "value1")
    clock.sleep(2)  # key1 is now stale
    cache.set("key2", "value2")
    cache.set("key3", "value3")  # This should evict key2, reclaiming stale key1
    assert cache.get("key1") is None  # AC-5.3: key1 should be stale and not returned
    assert cache.get("key2") == "value2"  # AC-5.3: key2 should remain
    assert cache.get("key3") == "value3"  # AC-5.3: key3 should remain

def test_remove_live_key_reports_success():
    cache = Cache()
    cache.set("key1", "value1")
    success = cache.remove("key1")  # Remove live key1
    assert success  # AC-5.4: Removing live key should succeed
    assert cache.get("key1") is None  # AC-5.4: key1 should be absent

def test_remove_absent_key_reports_failure():
    cache = Cache()
    success = cache.remove("absent_key")  # Try to remove absent key
    assert not success  # AC-5.5: Removing absent key should fail

def test_remove_stale_key_reports_failure(clock):
    cache = Cache(ttl=2, clock=clock)
    cache.set("key1", "value1")
    clock.sleep(2)
    success = cache.remove("key1")  # Try to remove stale key1
    assert not success  # AC-5.5: Removing stale key should fail

def test_clear_cache_leaves_no_entries():
    cache = Cache()
    cache.set("key1", "value1")
    cache.clear()  # Clear the cache
    assert cache.count() == 0  # AC-5.6: Count should be 0 after clear