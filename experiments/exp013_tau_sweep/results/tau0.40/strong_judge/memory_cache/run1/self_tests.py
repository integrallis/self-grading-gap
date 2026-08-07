# your complete test file
import pytest
import time
from solution import Cache

def test_default_configuration():
    cache = Cache()
    # AC-1.1: Default capacity is 100 and default ttl is 60 seconds
    assert cache.get('any_key') is None  # Cache is empty, should return None

def test_configurable_capacity_and_ttl():
    cache = Cache(capacity=50, ttl=30)
    assert cache.get('any_key') is None  # Cache is empty, should return None

def test_invalid_capacity_below_one():
    with pytest.raises(ValueError) as exc:
        Cache(capacity=0)  # AC-1.3: Reject capacity below 1
    assert str(exc.value) == "capacity must be at least 1, got [0]"

    with pytest.raises(ValueError) as exc:
        Cache(capacity=-1)  # AC-1.3: Reject capacity below 1
    assert str(exc.value) == "capacity must be at least 1, got [-1]"

def test_invalid_ttl_zero_or_negative():
    with pytest.raises(ValueError) as exc:
        Cache(ttl=0)  # AC-1.4: Reject zero ttl
    assert str(exc.value) == "ttl must be positive, got [0]"

    with pytest.raises(ValueError) as exc:
        Cache(ttl=-1.5)  # AC-1.4: Reject negative ttl
    assert str(exc.value) == "ttl must be positive, got [-1.5]"

def test_valid_ttl_positive():
    cache = Cache(ttl=1)  # AC-1.5: Accept positive ttl
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'  # Check that value is stored

def test_valid_ttl_fractional():
    cache = Cache(ttl=0.5)  # AC-1.5: Accept positive fractional ttl
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'  # Check that value is stored

def test_store_and_retrieve():
    cache = Cache()
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'  # AC-2.1: Retrieve stored value

def test_retrieve_absent_key_without_fallback():
    cache = Cache()
    assert cache.get('absent_key') is None  # AC-2.2: Absent key yields None by default

def test_retrieve_absent_key_with_fallback():
    cache = Cache()
    assert cache.get('absent_key', 'fallback') == 'fallback'  # AC-2.2: Absent key with fallback

def test_store_existing_key_replaces_value():
    cache = Cache()
    cache.set('key1', 'value1')
    cache.set('key1', 'value2')
    assert cache.get('key1') == 'value2'  # AC-2.3: Replacing existing key's value

def test_store_existing_key_does_not_increase_count():
    cache = Cache(capacity=2)
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'  # AC-2.3: key1 should exist
    assert cache.get('key1') is not None  # Entry count should not increase

def test_eviction_of_least_recently_used_entry():
    cache = Cache(capacity=2)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')  # Should evict key1
    assert cache.get('key1') is None  # AC-3.1: key1 should be evicted
    assert cache.get('key2') == 'value2'  # AC-3.1: key2 should still exist
    assert cache.get('key3') == 'value3'  # AC-3.1: key3 should exist

def test_reading_key_refreshes_recency():
    cache = Cache(capacity=2)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.get('key1')  # Accessing key1
    cache.set('key3', 'value3')  # Should evict key2 now
    assert cache.get('key2') is None  # AC-3.2: key2 should be evicted
    assert cache.get('key1') == 'value1'  # AC-3.2: key1 should still exist
    assert cache.get('key3') == 'value3'  # AC-3.2: key3 should exist

def test_rewriting_key_refreshes_recency():
    cache = Cache(capacity=2)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key1', 'value1_updated')  # Rewriting key1
    cache.set('key3', 'value3')  # Should evict key2
    assert cache.get('key1') == 'value1_updated'  # AC-3.3: key1 should reflect new value
    assert cache.get('key2') is None  # AC-3.3: key2 should be evicted
    assert cache.get('key3') == 'value3'  # AC-3.3: key3 should exist

def test_single_capacity_eviction():
    cache = Cache(capacity=1)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')  # Should evict key1
    assert cache.get('key1') is None  # AC-3.4: key1 should be evicted
    assert cache.get('key2') == 'value2'  # AC-3.4: key2 should exist

def test_entry_expiry():
    clock = time.time  # Using time as a clock
    cache = Cache(ttl=1)
    cache.set('key1', 'value1')
    time.sleep(0.5)  # Wait for half the ttl
    assert cache.get('key1') == 'value1'  # Entry should still be valid
    time.sleep(0.5)  # Wait for the entry to expire
    assert cache.get('key1') is None  # AC-4.1: key1 should be stale

def test_entry_still_served_before_expiry():
    clock = time.time  # Using time as a clock
    cache = Cache(ttl=1)
    cache.set('key1', 'value1')
    time.sleep(0.9)  # Wait just before expiry
    assert cache.get('key1') == 'value1'  # AC-4.2: key1 should still be served

def test_rewriting_key_restarts_ttl():
    clock = time.time  # Using time as a clock
    cache = Cache(ttl=1)
    cache.set('key1', 'value1')
    time.sleep(0.5)
    cache.set('key1', 'value1_updated')  # Rewriting key1
    time.sleep(0.5)  # Wait for the new ttl to expire
    assert cache.get('key1') == 'value1_updated'  # AC-4.3: key1 should reflect new value and not be stale

def test_expired_key_accepts_fresh_value():
    clock = time.time  # Using time as a clock
    cache = Cache(ttl=1)
    cache.set('key1', 'value1')
    time.sleep(1)  # Wait for the entry to expire
    cache.set('key1', 'new_value1')  # Accept new value for expired key
    assert cache.get('key1') == 'new_value1'  # AC-4.4: key1 should have new value

def test_count_and_membership_with_stale_entries():
    clock = time.time  # Using time as a clock
    cache = Cache(capacity=2, ttl=1)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    time.sleep(1)  # Expire entries
    assert cache.get('key1') is None  # AC-5.1: key1 should be stale and absent
    assert cache.get('key2') is None  # AC-5.1: key2 should be stale and absent

def test_explicit_sweep_removes_stale_entries():
    clock = time.time  # Using time as a clock
    cache = Cache(capacity=2, ttl=1)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    time.sleep(1)  # Expire entries
    removed_count = cache.sweep()  # Remove stale entries
    assert removed_count == 2  # AC-5.2: Two stale entries should be removed
    assert cache.get('key1') is None  # AC-5.2: key1 should be absent after sweep
    assert cache.get('key2') is None  # AC-5.2: key2 should be absent after sweep

def test_inserting_into_full_cache_reclaims_stale_slots_first():
    clock = time.time  # Using time as a clock
    cache = Cache(capacity=2, ttl=1)
    cache.set('key1', 'value1')
    time.sleep(1)  # Expire key1
    cache.set('key2', 'value2')  # key1 should be stale, should not be evicted
    cache.set('key3', 'value3')  # This should evict key2
    assert cache.get('key1') is None  # AC-5.3: key1 should be stale and absent
    assert cache.get('key2') is None  # AC-5.3: key2 should be evicted
    assert cache.get('key3') == 'value3'  # AC-5.3: key3 should exist

def test_remove_live_key_reports_success():
    cache = Cache()
    cache.set('key1', 'value1')
    assert cache.remove('key1') == True  # AC-5.4: Removing live key should succeed
    assert cache.get('key1') is None  # AC-5.4: key1 should be absent after removal

def test_remove_absent_key_reports_failure():
    cache = Cache()
    assert cache.remove('absent_key') == False  # AC-5.5: Removing absent key should fail

def test_remove_key_exactly_at_expiry_boundary_reports_failure():
    clock = time.time  # Using time as a clock
    cache = Cache(ttl=1)
    cache.set('key1', 'value1')
    time.sleep(1)  # Wait for key1 to expire
    assert cache.remove('key1') == False  # AC-5.5: Removing expired key should fail

def test_clear_cache_leaves_no_entries():
    cache = Cache()
    cache.set('key1', 'value1')
    cache.clear()  # AC-5.6: Clear the cache
    assert cache.get('key1') is None  # AC-5.6: Cache should be empty