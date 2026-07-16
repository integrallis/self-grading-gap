import pytest

from solution import Cache

def test_default_configuration():
    cache = Cache()
    # AC-1.1: Default capacity is 100
    # AC-1.1: Default time-to-live is 60 seconds
    assert cache.retrieve("key1") is None  # Verify default behavior

def test_custom_configuration():
    cache = Cache(capacity=50, ttl=30)
    # AC-1.2: Custom capacity
    # AC-1.2: Custom time-to-live
    assert cache.retrieve("key1") is None  # Verify custom behavior

def test_capacity_below_one_rejected():
    # AC-1.3: Zero capacity is rejected
    cache = Cache(capacity=0)  
    assert cache.retrieve("key1") is None  # Verify default behavior

    # AC-1.3: Negative capacity is rejected
    cache = Cache(capacity=-1)  
    assert cache.retrieve("key1") is None  # Verify default behavior

def test_zero_or_negative_ttl_rejected():
    # AC-1.4: Zero TTL is rejected
    cache = Cache(ttl=0)  
    assert cache.retrieve("key1") is None  # Verify default behavior

    # AC-1.4: Negative TTL is rejected
    cache = Cache(ttl=-1)  
    assert cache.retrieve("key1") is None  # Verify default behavior

def test_positive_ttl_accepted():
    cache = Cache(ttl=0.5)  # Testing a sub-second TTL
    assert cache.retrieve("key1") is None  # Verify default behavior

def test_store_and_retrieve_value():
    cache = Cache()
    cache.store("key1", "value1")
    # AC-2.1: Retrieve stored value
    assert cache.retrieve("key1") == "value1"  

def test_retrieve_absent_key():
    cache = Cache()
    # AC-2.2: Default return for absent key
    assert cache.retrieve("absent_key") is None  
    # AC-2.2: Return fallback for absent key
    assert cache.retrieve("absent_key", "fallback") == "fallback"  

def test_store_existing_key_replaces_value():
    cache = Cache()
    cache.store("key1", "value1")
    cache.store("key1", "value2")
    # AC-2.3: Existing key value replaced
    assert cache.retrieve("key1") == "value2"  
    # Check that entry count remains the same
    assert cache.count() == 1  # AC-2.3: Count should not increase

def test_least_recently_used_eviction():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key3", "value3")  # Cache is full; key1 should be evicted
    # AC-3.1: Key1 should be evicted
    assert cache.retrieve("key1") is None  
    # AC-3.1: Key2 is still available
    assert cache.retrieve("key2") == "value2"  
    # AC-3.1: Key3 is still available
    assert cache.retrieve("key3") == "value3"  

def test_reading_key_refreshes_recency():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.retrieve("key1")  # Refresh key1
    cache.store("key3", "value3")  # Should evict key2, not key1
    # AC-3.2: Key2 should be evicted
    assert cache.retrieve("key2") is None  
    # AC-3.2: Key1 is still available
    assert cache.retrieve("key1") == "value1"  
    # AC-3.2: Key3 is still available
    assert cache.retrieve("key3") == "value3"  

def test_rewriting_existing_key_refreshes_recency():
    cache = Cache(capacity=2)
    cache.store("key1", "value1")
    cache.store("key2", "value2")
    cache.store("key1", "value1_updated")  # Rewrite key1
    cache.store("key3", "value3")  # Should evict key2
    # AC-3.3: Key2 should be evicted
    assert cache.retrieve("key2") is None  
    # AC-3.3: Key1 is updated
    assert cache.retrieve("key1") == "value1_updated"  

def test_capacity_of_one_eviction():
    cache = Cache(capacity=1)
    cache.store("key1", "value1")
    cache.store("key2", "value2")  # Should evict key1
    # AC-3.4: Key1 should be evicted
    assert cache.retrieve("key1") is None  
    # AC-3.4: Key2 is available
    assert cache.retrieve("key2") == "value2"  

def test_entry_expiry_with_controlled_clock():
    clock = [0]  # Mutable list to act as a clock
    cache = Cache(ttl=1, clock=lambda: clock[0])

    def advance_clock(seconds):
        clock[0] += seconds

    cache.store("key1", "value1")
    advance_clock(1.1)  # Advance clock past expiry
    # AC-4.1: Key1 should be stale
    assert cache.retrieve("key1") is None  

def test_entry_not_expired_before_boundary_with_controlled_clock():
    clock = [0]  # Mutable list to act as a clock
    cache = Cache(ttl=1, clock=lambda: clock[0])

    def advance_clock(seconds):
        clock[0] += seconds

    cache.store("key1", "value1")
    advance_clock(0.9)  # Advance clock just before expiration
    # AC-4.2: Key1 should still be available
    assert cache.retrieve("key1") == "value1"  

def test_rewriting_key_resets_ttl_with_controlled_clock():
    clock = [0]  # Mutable list to act as a clock
    cache = Cache(ttl=1, clock=lambda: clock[0])

    def advance_clock(seconds):
        clock[0] += seconds

    cache.store("key1", "value1")
    advance_clock(0.5)  # Advance clock halfway
    cache.store("key1", "value1_updated")  # Rewrite key1
    advance_clock(0.5)  # Advance clock until expiration
    # AC-4.3: Key1 should still be available
    assert cache.retrieve("key1") == "value1_updated"  

def test_expired_key_accepts_fresh_value_with_controlled_clock():
    clock = [0]  # Mutable list to act as a clock
    cache = Cache(ttl=1, clock=lambda: clock[0])

    def advance_clock(seconds):
        clock[0] += seconds

    cache.store("key1", "value1")
    advance_clock(1.1)  # Advance clock past expiry
    cache.store("key1", "value1_new")  # Adding a fresh value
    # AC-4.4: New value should be available
    assert cache.retrieve("key1") == "value1_new"  

def test_entry_count_treats_stale_entries_as_absent_with_controlled_clock():
    clock = [0]  # Mutable list to act as a clock
    cache = Cache(clock=lambda: clock[0])
    
    def advance_clock(seconds):
        clock[0] += seconds

    cache.store("key1", "value1")
    cache.store("key2", "value2")
    advance_clock(60.1)  # Advance clock past expiration
    # AC-5.1: Count should be 0 for stale entries
    assert cache.count() == 0  

def test_sweep_removes_stale_entries_with_controlled_clock():
    clock = [0]  # Mutable list to act as a clock
    cache = Cache(clock=lambda: clock[0])

    def advance_clock(seconds):
        clock[0] += seconds

    cache.store("key1", "value1")
    cache.store("key2", "value2")
    advance_clock(60.1)  # Advance clock past expiration
    # AC-5.2: Sweep should remove 2 entries
    assert cache.sweep() == 2  
    # Cache should be empty
    assert cache.count() == 0  

def test_full_cache_reclaims_stale_slots_with_controlled_clock():
    clock = [0]  # Mutable list to act as a clock
    cache = Cache(capacity=2, ttl=1, clock=lambda: clock[0])

    def advance_clock(seconds):
        clock[0] += seconds

    cache.store("key1", "value1")
    advance_clock(1.1)  # Advance clock enough for key1 to expire
    cache.store("key2", "value2")  # key1 is stale, should be reclaimed
    cache.store("key3", "value3")  # Should evict key2, but reclaim key1
    # Key1 should be stale
    assert cache.retrieve("key1") is None  
    # Key2 should be evicted
    assert cache.retrieve("key2") is None  
    # Key3 should be available
    assert cache.retrieve("key3") == "value3"  

def test_remove_live_key_reports_success():
    cache = Cache()
    cache.store("key1", "value1")
    # AC-5.4: Removing live key should succeed
    assert cache.remove("key1") is True  
    # Key1 should be absent
    assert cache.retrieve("key1") is None  

def test_remove_absent_key_reports_failure():
    cache = Cache()
    # AC-5.5: Removing absent key should fail
    assert cache.remove("absent_key") is False  

def test_remove_stale_key_reports_failure_with_controlled_clock():
    clock = [0]  # Mutable list to act as a clock
    cache = Cache(ttl=1, clock=lambda: clock[0])

    def advance_clock(seconds):
        clock[0] += seconds

    cache.store("key1", "value1")
    advance_clock(1.1)  # Advance clock past expiry
    # AC-5.5: Removing expired key should fail
    assert cache.remove("key1") is False  

def test_remove_key_at_expiry_boundary_reports_failure_with_controlled_clock():
    clock = [0]  # Mutable list to act as a clock
    cache = Cache(ttl=1, clock=lambda: clock[0])

    def advance_clock(seconds):
        clock[0] += seconds

    cache.store("key1", "value1")
    advance_clock(1)  # Advance clock to exactly the expiry time
    # Should return False as it is now stale
    assert cache.remove("key1") is False  

def test_clear_cache_leaves_no_entries():
    cache = Cache()
    cache.store("key1", "value1")
    cache.clear()  # AC-5.6: Clearing the cache
    # Cache should be empty
    assert cache.count() == 0