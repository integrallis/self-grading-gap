import time
import pytest
from solution import Cache  # Assuming the class to be tested is named Cache


def test_default_configuration():
    cache = Cache()
    assert cache.capacity == 100
    assert cache.ttl == 60


def test_configurable_capacity_and_ttl():
    cache = Cache(capacity=50, ttl=30)
    assert cache.capacity == 50
    assert cache.ttl == 30


def test_reject_capacity_below_one():
    with pytest.raises(ValueError) as excinfo:
        Cache(capacity=0)
    assert str(excinfo.value) == "capacity must be at least 1, got [0]"

    with pytest.raises(ValueError) as excinfo:
        Cache(capacity=-5)
    assert str(excinfo.value) == "capacity must be at least 1, got [-5]"


def test_reject_zero_or_negative_ttl():
    with pytest.raises(ValueError) as excinfo:
        Cache(ttl=0)
    assert str(excinfo.value) == "ttl must be positive, got [0]"

    with pytest.raises(ValueError) as excinfo:
        Cache(ttl=-1)
    assert str(excinfo.value) == "ttl must be positive, got [-1]"


def test_accept_positive_ttl():
    cache = Cache(ttl=1)
    assert cache.ttl == 1

    cache = Cache(ttl=60)
    assert cache.ttl == 60


def test_store_and_retrieve_value():
    cache = Cache()
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'  # Expected: 'value1'


def test_retrieve_absent_key_with_default_fallback():
    cache = Cache()
    assert cache.get('absent_key', 'fallback') == 'fallback'  # Expected: 'fallback'


def test_overwrite_existing_key():
    cache = Cache()
    cache.set('key1', 'value1')
    cache.set('key1', 'value2')
    assert cache.get('key1') == 'value2'  # Expected: 'value2'


def test_eviction_when_full():
    cache = Cache(capacity=2)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')  # Evicts 'key1'
    assert cache.get('key1') is None  # Expected: None
    assert cache.get('key2') == 'value2'  # Expected: 'value2'
    assert cache.get('key3') == 'value3'  # Expected: 'value3'


def test_reading_key_refreshes_recency():
    cache = Cache(capacity=2)
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.get('key1')  # Refresh 'key1'
    cache.set('key3', 'value3')  # Should evict 'key2'
    assert cache.get('key2') is None  # Expected: None
    assert cache.get('key1') == 'value1'  # Expected: 'value1'
    assert cache.get('key3') == 'value3'  # Expected: 'value3'


def test_rewriting_key_refreshes_ttl():
    cache = Cache(ttl=2)
    cache.set('key1', 'value1')
    time.sleep(1)
    cache.set('key1', 'value2')  # Refresh TTL
    time.sleep(2)  # Now the key should still be valid
    assert cache.get('key1') == 'value2'  # Expected: 'value2'


def test_stale_entry():
    cache = Cache(ttl=1)
    cache.set('key1', 'value1')
    time.sleep(1)  # Wait for expiry
    assert cache.get('key1') is None  # Expected: None


def test_expiry_boundary():
    cache = Cache(ttl=1)
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'  # Expected: 'value1'
    time.sleep(1)  # Wait for expiry
    assert cache.get('key1') is None  # Expected: None


def test_expiry_on_rewrite():
    cache = Cache(ttl=1)
    cache.set('key1', 'value1')
    time.sleep(0.5)
    cache.set('key1', 'value2')  # Refresh TTL
    time.sleep(1)  # Now the key should still be valid
    assert cache.get('key1') == 'value2'  # Expected: 'value2'


def test_removing_live_key():
    cache = Cache()
    cache.set('key1', 'value1')
    assert cache.remove('key1') is True  # Expected: True
    assert cache.get('key1') is None  # Expected: None


def test_removing_absent_key():
    cache = Cache()
    assert cache.remove('absent_key') is False  # Expected: False


def test_removing_stale_key():
    cache = Cache(ttl=1)
    cache.set('key1', 'value1')
    time.sleep(1)  # Wait for expiry
    assert cache.remove('key1') is False  # Expected: False


def test_clear_cache():
    cache = Cache()
    cache.set('key1', 'value1')
    cache.clear()
    assert cache.get('key1') is None  # Expected: None