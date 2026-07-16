from solution import Cache

def test_default_configuration():
    cache = Cache()
    assert cache.capacity == 100  # AC-1.1
    assert cache.ttl == 60  # AC-1.1

def test_configurable_capacity_and_ttl():
    cache = Cache(capacity=50, ttl=30)
    assert cache.capacity == 50  # AC-1.2
    assert cache.ttl == 30  # AC-1.2

def test_invalid_capacity_below_one():
    with pytest.raises(ValueError) as excinfo:
        Cache(capacity=0)
    assert str(excinfo.value) == "capacity must be at least 1, got [0]"  # AC-1.3

    with pytest.raises(ValueError) as excinfo:
        Cache(capacity=-1)
    assert str(excinfo.value) == "capacity must be at least 1, got [-1]"  # AC-1.3

def test_invalid_ttl_zero_or_negative():
    with pytest.raises(ValueError) as excinfo:
        Cache(ttl=0)
    assert str(excinfo.value) == "ttl must be positive, got [0]"  # AC-1.4

    with pytest.raises(ValueError) as excinfo:
        Cache(ttl=-1)
    assert str(excinfo.value) == "ttl must be positive, got [-1]"  # AC-1.4

def test_valid_ttl_positive():
    cache = Cache(ttl=1)  # AC-1.5
    assert cache.ttl == 1  # AC-1.5

def test_store_and_retrieve():
    cache = Cache()
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"  # AC-2.1

def test_retrieve_absent_key():
    cache = Cache()
    assert cache.get("absent_key") is None  # AC-2.2
    assert cache.get("absent_key", "fallback") == "fallback"  # AC-2.2

def test_store_existing_key_replaces_value():
    cache = Cache()
    cache.set("key1", "value1")
    cache.set("key1", "value2")
    assert cache.get("key1") == "value2"  # AC-2.3

def test_least_recently_used_eviction():
    cache = Cache(capacity=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")  # key1 should be evicted
    assert cache.get("key1") is None  # AC-3.1
    assert cache.get("key2") == "value2"  # AC-3.1
    assert cache.get("key3") == "value3"  # AC-3.1

def test_read_refreshes_recency():
    cache = Cache(capacity=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.get("key1")  # refresh key1
    cache.set("key3", "value3")  # key2 should be evicted
    assert cache.get("key2") is None  # AC-3.2
    assert cache.get("key1") == "value1"  # AC-3.2
    assert cache.get("key3") == "value3"  # AC-3.2

def test_rewriting_key_refreshes_recency():
    cache = Cache(capacity=2)
    cache.set("key1", "value1")
    cache.set("key1", "value2")  # rewrite key1
    cache.set("key2", "value2")
    cache.set("key3", "value3")  # key1 should stay, key2 evicted
    assert cache.get("key2") is None  # AC-3.3
    assert cache.get("key1") == "value2"  # AC-3.3
    assert cache.get("key3") == "value3"  # AC-3.3

def test_capacity_of_one_replaces_previous_entry():
    cache = Cache(capacity=1)
    cache.set("key1", "value1")
    cache.set("key2", "value2")  # replaces key1
    assert cache.get("key1") is None  # AC-3.4
    assert cache.get("key2") == "value2"  # AC-3.4

def test_entry_expiry():
    cache = Cache(ttl=1)
    cache.set("key1", "value1")
    time.sleep(1)  # wait for expiry
    assert cache.get("key1") is None  # AC-4.1

def test_entry_not_expired_before_boundary():
    cache = Cache(ttl=1)
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"  # AC-4.2
    time.sleep(0.5)
    assert cache.get("key1") == "value1"  # AC-4.2

def test_rewriting_key_restores_ttl():
    cache = Cache(ttl=1)
    cache.set("key1", "value1")
    time.sleep(0.5)
    cache.set("key1", "value2")  # reset ttl
    time.sleep(0.5)
    assert cache.get("key1") == "value2"  # AC-4.3
    time.sleep(0.5)
    assert cache.get("key1") is None  # AC-4.3

def test_stale_key_accepts_fresh_value():
    cache = Cache(ttl=1)
    cache.set("key1", "value1")
    time.sleep(1)  # wait for expiry
    cache.set("key1", "new_value")  # should accept fresh value
    assert cache.get("key1") == "new_value"  # AC-4.4

def test_entry_count_treats_stale_entries_as_absent():
    cache = Cache(capacity=2, ttl=1)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    time.sleep(1)  # expire entries
    assert cache.count() == 0  # AC-5.1

def test_membership_check_treats_stale_entries_as_absent():
    cache = Cache(capacity=2, ttl=1)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    time.sleep(1)  # expire entries
    assert not cache.has("key1")  # AC-5.1
    assert not cache.has("key2")  # AC-5.1

def test_explicit_sweep_removes_stale_entries():
    cache = Cache(capacity=2, ttl=1)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    time.sleep(1)  # expire entries
    removed_count = cache.sweep()  # AC-5.2
    assert removed_count == 2  # AC-5.2
    assert cache.count() == 0  # AC-5.2

def test_full_cache_reclaims_stale_slots_first():
    cache = Cache(capacity=2, ttl=1)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    time.sleep(1)  # expire entries
    cache.set("key3", "value3")  # should reclaim stale key slots
    assert cache.get("key3") == "value3"  # AC-5.3
    assert cache.get("key1") is None  # AC-5.3
    assert cache.get("key2") is None  # AC-5.3

def test_remove_live_key_reports_success():
    cache = Cache()
    cache.set("key1", "value1")
    assert cache.remove("key1") is True  # AC-5.4
    assert cache.get("key1") is None  # AC-5.4

def test_remove_absent_key_reports_failure():
    cache = Cache()
    assert cache.remove("absent_key") is False  # AC-5.5

def test_remove_key_exactly_at_expiry_boundary_reports_failure():
    cache = Cache(ttl=1)
    cache.set("key1", "value1")
    time.sleep(1)  # wait for expiry
    assert cache.remove("key1") is False  # AC-5.5

def test_clear_empty_cache():
    cache = Cache()
    cache.clear()  # should leave it with no entries
    assert cache.count() == 0  # AC-5.6

def test_clear_non_empty_cache():
    cache = Cache()
    cache.set("key1", "value1")
    cache.clear()  # should leave it with no entries
    assert cache.count() == 0  # AC-5.6