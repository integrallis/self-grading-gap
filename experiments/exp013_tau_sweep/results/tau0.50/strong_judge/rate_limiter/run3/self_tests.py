import pytest
from solution import *  # Import everything from the solution package

def test_first_request_approved():
    throttler = Throttler(max_requests=3, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # First request should be approved

def test_within_quota_requests_approved():
    throttler = Throttler(max_requests=3, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # First request should be approved
    assert throttler.is_request_approved("client1")  # Second request should be approved
    assert throttler.is_request_approved("client1")  # Third request should be approved

def test_exceeding_quota_request_denied():
    throttler = Throttler(max_requests=3, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # First request should be approved
    assert throttler.is_request_approved("client1")  # Second request should be approved
    assert throttler.is_request_approved("client1")  # Third request should be approved
    assert not throttler.is_request_approved("client1")  # Fourth request should be denied

def test_one_request_per_window():
    throttler = Throttler(max_requests=1, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # First request approved
    assert not throttler.is_request_approved("client1")  # Second request denied

def test_different_clients_isolated():
    throttler = Throttler(max_requests=3, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # Client 1 approved
    assert throttler.is_request_approved("client2")  # Client 2 approved
    assert throttler.is_request_approved("client1")  # Client 1 approved again
    assert throttler.is_request_approved("client1")  # Client 1 approved again
    assert not throttler.is_request_approved("client1")  # Client 1 denied
    assert throttler.is_request_approved("client2")  # Client 2 still approved

def test_interleaved_requests_accounted_per_client():
    throttler = Throttler(max_requests=2, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # Client 1 approved
    assert throttler.is_request_approved("client2")  # Client 2 approved
    assert throttler.is_request_approved("client1")  # Client 1 approved
    assert not throttler.is_request_approved("client1")  # Client 1 denied
    assert throttler.is_request_approved("client2")  # Client 2 still approved

def test_requests_older_than_window_no_longer_count():
    throttler = Throttler(max_requests=2, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # Approved at time 0
    throttler.time_source.advance(11)  # Advance time by more than the time window
    assert throttler.is_request_approved("client1")  # Should be approved again

def test_request_at_boundary_no_longer_counts():
    throttler = Throttler(max_requests=1, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # Approved at time 0
    throttler.time_source.advance(10)  # Advance time to exactly the time window
    assert throttler.is_request_approved("client1")  # Should be approved again

def test_request_less_than_window_still_counts():
    throttler = Throttler(max_requests=2, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # Approved at time 0
    throttler.time_source.advance(5)  # Advance time to less than the time window
    assert throttler.is_request_approved("client1")  # Still counts, should be approved
    assert not throttler.is_request_approved("client1")  # Third request should be denied

def test_expiry_per_request():
    throttler = Throttler(max_requests=3, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # Approved at time 0
    throttler.time_source.advance(4)  # Advance time by 4 seconds
    assert throttler.is_request_approved("client1")  # Approved at time 4
    throttler.time_source.advance(4)  # Advance time by another 4 seconds
    assert not throttler.is_request_approved("client1")  # Should be denied
    throttler.time_source.advance(2)  # Wait for 2 more seconds
    assert throttler.is_request_approved("client1")  # Should be approved again after inactivity

def test_denied_requests_do_not_count():
    throttler = Throttler(max_requests=1, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # Approved at time 0
    assert not throttler.is_request_approved("client1")  # Denied
    throttler.time_source.advance(10)  # Wait for the time window
    assert throttler.is_request_approved("client1")  # Should be approved again after 10 seconds

def test_quota_below_one_rejected():
    with pytest.raises(Exception) as excinfo:
        Throttler(max_requests=-1, time_window=10, time_source=MockTimeSource())
    assert str(excinfo.value) == "max_requests must be positive"

def test_zero_or_negative_window_rejected():
    with pytest.raises(Exception) as excinfo:
        Throttler(max_requests=3, time_window=0, time_source=MockTimeSource())
    assert str(excinfo.value) == "time_window must be positive"
    with pytest.raises(Exception) as excinfo:
        Throttler(max_requests=3, time_window=-10, time_source=MockTimeSource())
    assert str(excinfo.value) == "time_window must be positive"

def test_positive_window_length_accepted():
    throttler = Throttler(max_requests=3, time_window=2.5, time_source=MockTimeSource())  # Accept fraction of a second
    assert throttler.is_request_approved("client1")  # First request should be approved

def test_full_window_of_inactivity():
    throttler = Throttler(max_requests=3, time_window=10, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # Approved at time 0
    assert throttler.is_request_approved("client1")  # Approved at time 0
    assert throttler.is_request_approved("client1")  # Approved at time 0
    throttler.time_source.advance(10)  # Wait for the entire window
    assert throttler.is_request_approved("client1")  # Should be approved again after inactivity

def test_fractional_window_expiry():
    throttler = Throttler(max_requests=1, time_window=0.5, time_source=MockTimeSource())
    assert throttler.is_request_approved("client1")  # Approved at time 0
    throttler.time_source.advance(0.5)  # Advance time to the exact boundary
    assert throttler.is_request_approved("client1")  # Should be approved again