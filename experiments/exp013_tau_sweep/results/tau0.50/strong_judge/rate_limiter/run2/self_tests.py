import pytest
from solution import Throttle

def test_client_first_request_approved():
    throttle = Throttle(max_requests=3, time_window=10)
    assert throttle.request("client1") == "approved"  # First request, should be approved

def test_client_within_quota_requests_approved():
    throttle = Throttle(max_requests=3, time_window=10)
    throttle.request("client1")  # First request
    assert throttle.request("client1") == "approved"  # Within quota
    assert throttle.request("client1") == "approved"  # Within quota

def test_client_exceeding_quota_request_denied():
    throttle = Throttle(max_requests=3, time_window=10)
    throttle.request("client1")  # First request
    throttle.request("client1")  # Second request
    throttle.request("client1")  # Third request
    assert throttle.request("client1") == "denied"  # Exceeds quota, should be denied

def test_quota_of_one_request_approved_per_window():
    throttle = Throttle(max_requests=1, time_window=10)
    assert throttle.request("client1") == "approved"  # First request
    assert throttle.request("client1") == "denied"  # Denied within the same window
    assert throttle.request("client1") == "approved"  # Approved after window expires

def test_client_denied_for_exhausting_quota_does_not_affect_other_clients():
    throttle = Throttle(max_requests=2, time_window=10)
    throttle.request("client1")  # Approved
    throttle.request("client1")  # Approved
    assert throttle.request("client1") == "denied"  # Denied
    assert throttle.request("client2") == "approved"  # Client 2 should be approved

def test_interleaved_traffic_accounted_per_client():
    throttle = Throttle(max_requests=2, time_window=10)
    assert throttle.request("client1") == "approved"
    assert throttle.request("client2") == "approved"
    assert throttle.request("client1") == "approved"
    assert throttle.request("client2") == "approved"
    assert throttle.request("client1") == "denied"  # Client 1 exceeds quota
    assert throttle.request("client2") == "denied"  # Client 2 exceeds quota

def test_requests_older_than_window_no_longer_count():
    throttle = Throttle(max_requests=2, time_window=10)
    assert throttle.request("client1") == "approved"
    assert throttle.request("client1") == "approved"
    assert throttle.request("client1") == "approved"  # Window has slid, should be approved

def test_request_aged_exactly_one_window_length_no_longer_count():
    throttle = Throttle(max_requests=2, time_window=10)
    assert throttle.request("client1") == "approved"
    assert throttle.request("client1") == "approved"  # Exactly one window length, should be approved

def test_request_aged_less_than_one_window_length_still_counts():
    throttle = Throttle(max_requests=2, time_window=10)
    assert throttle.request("client1") == "approved"
    assert throttle.request("client1") == "approved"  # Within quota
    assert throttle.request("client1") == "denied"  # Still counts against quota

def test_expiry_is_per_request():
    throttle = Throttle(max_requests=3, time_window=10)
    assert throttle.request("client1") == "approved"  # Approved
    assert throttle.request("client1") == "approved"  # Approved
    assert throttle.request("client1") == "approved"  # Approved
    assert throttle.request("client1") == "denied"  # Denied, quota exhausted
    assert throttle.request("client1") == "approved"  # One request has aged out, approved
    assert throttle.request("client1") == "denied"  # Denied again, proving one slot was consumed

def test_full_window_of_inactivity_resets_quota():
    throttle = Throttle(max_requests=2, time_window=10)
    assert throttle.request("client1") == "approved"
    assert throttle.request("client1") == "approved"
    assert throttle.request("client1") == "approved"  # Full window of inactivity, should be reset

def test_denied_request_does_not_consume_quota():
    throttle = Throttle(max_requests=1, time_window=10)
    assert throttle.request("client1") == "approved"  # Approved
    assert throttle.request("client1") == "denied"  # Denied
    assert throttle.request("client1") == "approved"  # Approved again, denial does not count

def test_invalid_quota_below_one_rejected():
    with pytest.raises(Exception) as exc:
        Throttle(max_requests=-1, time_window=10)
    assert str(exc.value) == "max_requests must be positive"

    with pytest.raises(Exception) as exc:
        Throttle(max_requests=0, time_window=10)
    assert str(exc.value) == "max_requests must be positive"

def test_invalid_time_window_zero_or_negative_rejected():
    with pytest.raises(Exception) as exc:
        Throttle(max_requests=1, time_window=0)
    assert str(exc.value) == "time_window must be positive"

    with pytest.raises(Exception) as exc:
        Throttle(max_requests=1, time_window=-5)
    assert str(exc.value) == "time_window must be positive"

def test_valid_time_window_fractional_seconds_accepted():
    throttle = Throttle(max_requests=1, time_window=0.5)  # Should be accepted
    assert throttle.request("client1") == "approved"
    assert throttle.request("client1") == "denied"  # Denied within the window
    assert throttle.request("client1") == "approved"  # Approved after window expires