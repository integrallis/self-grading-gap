from solution import Cache

def test_cache_default_configuration():
    cache = Cache()
    assert cache.capacity == 100  # AC-1.1: Default maximum of 100 entries
    assert cache.ttl == 60  # AC-1.1: Default time-to-live of 60 seconds

def test_cache_custom_configuration():
    cache = Cache(capacity=50, ttl=30)
    assert cache.capacity == 50  # AC-1.2: Custom capacity
    assert cache.ttl == 30  # AC-1.2: Custom time-to-live

def test_cache_capacity_below_one():
    with pytest.raises(ValueError, match="capacity must be at least 1, got [0]"):
        Cache(capacity=0)  # AC-1.3: Reject zero capacity
    with pytest.raises(ValueError, match="capacity must be at least 1, got [-1]"):
        Cache(capacity=-1)  # AC-1.3: Reject negative capacity

def test_cache_negative_or_zero_ttl():
    with pytest.raises(ValueError, match="ttl must be positive, got [0]"):
        Cache(ttl=0)  # AC-1.4: Reject zero TTL
    with pytest.raises(ValueError, match="ttl must be positive, got [-1]"):
        Cache(ttl=-1)  # AC-1.4: Reject negative TTL

def test_cache_positive_ttl():
    cache = Cache(ttl=1)  # AC-1.5: Accept TTL of one second
    assert cache.ttl == 1  # AC-1.5: Check TTL is set correctly

def test_cache_store_and_retrieve():
    cache = Cache()
    cache.store('key1', 'value1')
    assert cache.retrieve('key1') == 'value1'  # AC-2.1: Retrieve stored value

def test_cache_retrieve_absent_key():
    cache = Cache()
    assert cache.retrieve('absent_key') is None  # AC-2.2: Absent key yields None
    assert cache.retrieve('absent_key', fallback='default') == 'default'  # AC-2.2: Fallback value

def test_cache_overwrite_existing_key():
    cache = Cache()
    cache.store('key1', 'value1')
    cache.store('key1', 'value2')  # AC-2.3: Overwrite existing key
    assert cache.retrieve('key1') == 'value2'  # AC-2.3: Check value is updated

def test_cache_eviction_when_full():
    cache = Cache(capacity=2)
    cache.store('key1', 'value1')
    cache.store('key2', 'value2')
    cache.store('key3', 'value3')  # AC-3.1: Evict 'key1' (least recently used)
    assert cache.retrieve('key1') is None  # Check 'key1' is evicted
    assert cache.retrieve('key2') == 'value2'  # 'key2' should still be present
    assert cache.retrieve('key3') == 'value3'  # 'key3' should be present

def test_cache_refresh_recency_on_read():
    cache = Cache(capacity=2)
    cache.store('key1', 'value1')
    cache.store('key2', 'value2')
    cache.retrieve('key1')  # Refresh recency of 'key1'
    cache.store('key3', 'value3')  # AC-3.2: Evict 'key2'
    assert cache.retrieve('key2') is None  # 'key2' should be evicted
    assert cache.retrieve('key1') == 'value1'  # 'key1' should be present
    assert cache.retrieve('key3') == 'value3'  # 'key3' should be present

def test_cache_refresh_recency_on_write():
    cache = Cache(capacity=2)
    cache.store('key1', 'value1')
    cache.store('key2', 'value2')
    cache.store('key1', 'value1_updated')  # AC-3.3: Write to 'key1' refreshes it
    cache.store('key3', 'value3')  # Eviction should occur
    assert cache.retrieve('key2') is None  # 'key2' should be evicted
    assert cache.retrieve('key1') == 'value1_updated'  # 'key1' should be updated
    assert cache.retrieve('key3') == 'value3'  # 'key3' should be present

def test_cache_eviction_with_single_capacity():
    cache = Cache(capacity=1)
    cache.store('key1', 'value1')
    cache.store('key2', 'value2')  # AC-3.4: Evict 'key1'
    assert cache.retrieve('key1') is None  # 'key1' should be evicted
    assert cache.retrieve('key2') == 'value2'  # 'key2' should be present

def test_cache_entry_expiry():
    cache = Cache(ttl=1)  # 1 second TTL
    cache.store('key1', 'value1')
    assert cache.retrieve('key1') == 'value1'  # AC-4.2: Before expiry, entry is present
    time.sleep(1)  # Wait for expiry
    assert cache.retrieve('key1') is None  # AC-4.1: After expiry, entry is stale

def test_cache_rewrite_resets_ttl():
    cache = Cache(ttl=1)  # 1 second TTL
    cache.store('key1', 'value1')
    time.sleep(0.5)
    cache.store('key1', 'value1_updated')  # AC-4.3: Rewrite resets TTL
    time.sleep(0.5)
    assert cache.retrieve('key1') == 'value1_updated'  # Still present
    time.sleep(1)
    assert cache.retrieve('key1') is None  # Now expired

def test_cache_accepts_fresh_value_after_expiry():
    cache = Cache(ttl=1)
    cache.store('key1', 'value1')
    time.sleep(1)  # Expire key
    cache.store('key1', 'value1_fresh')  # AC-4.4: Accept fresh value
    assert cache.retrieve('key1') == 'value1_fresh'  # Verify fresh value is stored

def test_cache_count_and_membership_with_stale_entries():
    cache = Cache(capacity=2)
    cache.store('key1', 'value1')
    cache.store('key2', 'value2')
    time.sleep(1)  # Expire key1
    assert cache.count() == 1  # AC-5.1: Count should not include stale entries
    assert 'key1' not in cache  # Key1 is stale
    assert 'key2' in cache  # Key2 is live

def test_cache_explicit_sweep_removes_stale_entries():
    cache = Cache(capacity=2)
    cache.store('key1', 'value1')
    cache.store('key2', 'value2')
    time.sleep(1)  # Expire key1
    removed_count = cache.sweep()  # AC-5.2: Sweep should remove stale entries
    assert removed_count == 1  # One entry should be removed
    assert cache.count() == 1  # Should only have one live entry

def test_cache_eviction_of_stale_slots_first():
    cache = Cache(capacity=2, ttl=1)
    cache.store('key1', 'value1')
    time.sleep(1)  # Expire key1
    cache.store('key2', 'value2')  # Should reclaim stale slot for inserting key2
    assert cache.retrieve('key1') is None  # Key1 should be evicted
    assert cache.retrieve('key2') == 'value2'  # Key2 should be present

def test_cache_remove_live_key():
    cache = Cache()
    cache.store('key1', 'value1')
    assert cache.remove('key1') is True  # AC-5.4: Removing live key should succeed
    assert cache.retrieve('key1') is None  # Key1 should be absent now

def test_cache_remove_absent_key():
    cache = Cache()
    assert cache.remove('absent_key') is False  # AC-5.5: Removing absent key should fail

def test_cache_remove_stale_key():
    cache = Cache(ttl=1)
    cache.store('key1', 'value1')
    time.sleep(1)  # Expire key1
    assert cache.remove('key1') is False  # AC-5.5: Removing stale key should fail

def test_cache_clear():
    cache = Cache()
    cache.store('key1', 'value1')
    cache.store('key2', 'value2')
    cache.clear()  # AC-5.6: Clear the cache
    assert cache.count() == 0  # Cache should be empty