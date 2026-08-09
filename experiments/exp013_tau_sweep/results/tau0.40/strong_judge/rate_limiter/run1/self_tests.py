import pytest
from solution import Throttle

def test_first_request_approved():
    throttle = Throttle(max_requests=1, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # First request, should be approved

def test_within_quota_requests_approved():
    throttle = Throttle(max_requests=3, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # First request, should be approved
    assert throttle.request("client1") == True  # Second request, should be approved
    assert throttle.request("client1") == True  # Third request, should be approved

def test_exceeding_quota_request_denied():
    throttle = Throttle(max_requests=2, time_window=10, time_source=lambda: 0)
    throttle.request("client1")  # 1st request, approved
    throttle.request("client1")  # 2nd request, approved
    assert throttle.request("client1") == False  # 3rd request, should be denied

def test_quota_of_one_only_one_request_approved():
    throttle = Throttle(max_requests=1, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # First request, should be approved
    assert throttle.request("client1") == False  # Second request within the same window, should be denied

def test_different_clients_isolation():
    throttle = Throttle(max_requests=2, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # Client 1 first request
    assert throttle.request("client1") == True  # Client 1 second request
    assert throttle.request("client2") == True  # Client 2 first request, should be approved
    assert throttle.request("client2") == True  # Client 2 second request, should be approved
    assert throttle.request("client1") == False  # Client 1 third request, should be denied

def test_requests_aging_out():
    throttle = Throttle(max_requests=2, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # Approved at t=0
    throttle.time_source = lambda: 5  # Advance time to t=5
    assert throttle.request("client1") == True  # Approved at t=5
    throttle.time_source = lambda: 10  # Advance time to t=10
    assert throttle.request("client1") == True  # Approved at t=10, first request aged out

def test_requests_exactly_one_window_length_aging_out():
    throttle = Throttle(max_requests=2, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # Approved at t=0
    throttle.time_source = lambda: 10  # Advance time to t=10
    assert throttle.request("client1") == True  # Approved at t=10, first request aged out

def test_requests_less_than_one_window_length_count():
    throttle = Throttle(max_requests=2, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # Approved at t=0
    throttle.time_source = lambda: 5  # Advance time to t=5
    assert throttle.request("client1") == True  # Approved at t=5
    throttle.time_source = lambda: 9  # Advance time to t=9
    assert throttle.request("client1") == False  # Denied at t=9, quota is full
    throttle.time_source = lambda: 10  # Advance time to t=10
    assert throttle.request("client1") == True  # Approved at t=10, first request aged out

def test_expiry_per_request():
    throttle = Throttle(max_requests=3, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # Approved at t=0
    throttle.time_source = lambda: 2  # Advance time to t=2
    assert throttle.request("client1") == True  # Approved at t=2
    throttle.time_source = lambda: 8  # Advance time to t=8
    assert throttle.request("client1") == True  # Approved at t=8
    throttle.time_source = lambda: 9  # Advance time to t=9
    assert throttle.request("client1") == False  # Denied at t=9, quota is full
    throttle.time_source = lambda: 10  # Advance time to t=10
    assert throttle.request("client1") == True  # Approved at t=10, first request aged out

def test_full_window_of_inactivity_resets_quota():
    throttle = Throttle(max_requests=1, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # Approved at t=0
    throttle.time_source = lambda: 5  # Advance time to t=5
    assert throttle.request("client1") == False  # Denied at t=5
    throttle.time_source = lambda: 11  # Advance time to t=11
    assert throttle.request("client1") == True  # Approved at t=11, after a full window of inactivity

def test_denied_requests_do_not_consume_quota():
    throttle = Throttle(max_requests=1, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # Approved at t=0
    throttle.time_source = lambda: 5  # Advance time to t=5
    assert throttle.request("client1") == False  # Denied at t=5
    throttle.time_source = lambda: 10  # Advance time to t=10
    assert throttle.request("client1") == True  # Approved at t=10, denial did not consume quota

def test_invalid_quota_below_one():
    with pytest.raises(ValueError, match="^max_requests must be positive$"):
        Throttle(max_requests=0, time_window=10, time_source=lambda: 0)
    with pytest.raises(ValueError, match="^max_requests must be positive$"):
        Throttle(max_requests=-1, time_window=10, time_source=lambda: 0)

def test_invalid_time_window_zero_or_negative():
    with pytest.raises(ValueError, match="^time_window must be positive$"):
        Throttle(max_requests=1, time_window=0, time_source=lambda: 0)
    with pytest.raises(ValueError, match="^time_window must be positive$"):
        Throttle(max_requests=1, time_window=-1, time_source=lambda: 0)

def test_valid_fractional_time_window():
    throttle = Throttle(max_requests=1, time_window=0.5, time_source=lambda: 0)  # Should be accepted
    assert throttle.request("client1") == True  # Approved at t=0
    throttle.time_source = lambda: 0.5  # Advance time to t=0.5
    assert throttle.request("client1") == False  # Denied at t=0.5, window expired
    throttle.time_source = lambda: 0.6  # Advance time to t=0.6
    assert throttle.request("client1") == True  # Approved at t=0.6, after window aged out

def test_client_exhaustion_does_not_affect_others():
    throttle = Throttle(max_requests=2, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # Client 1 approved
    assert throttle.request("client1") == True  # Client 1 approved
    assert throttle.request("client1") == False  # Client 1 denied
    assert throttle.request("client2") == True  # Client 2 approved

def test_interleaved_traffic():
    throttle = Throttle(max_requests=2, time_window=10, time_source=lambda: 0)
    assert throttle.request("client1") == True  # Client 1 approved
    assert throttle.request("client2") == True  # Client 2 approved
    throttle.time_source = lambda: 5  # Advance time to t=5
    assert throttle.request("client1") == True  # Client 1 approved
    assert throttle.request("client2") == True  # Client 2 approved
    throttle.time_source = lambda: 10  # Advance time to t=10
    assert throttle.request("client1") == False  # Client 1 denied
    assert throttle.request("client2") == False  # Client 2 denied