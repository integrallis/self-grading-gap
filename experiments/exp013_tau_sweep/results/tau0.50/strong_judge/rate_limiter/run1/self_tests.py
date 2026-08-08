import pytest
from solution import Throttler  # Assuming the class to be tested is called Throttler

def test_first_request_approved():
    throttler = Throttler(max_requests=1, time_window=10)
    assert throttler.request("client1") is True  # First request should be approved

def test_subsequent_requests_within_quota_approved():
    throttler = Throttler(max_requests=2, time_window=10)
    throttler.request("client1")  # First request
    assert throttler.request("client1") is True  # Second request within quota should be approved

def test_exceeding_quota_denied():
    throttler = Throttler(max_requests=2, time_window=10)
    throttler.request("client1")  # First request
    throttler.request("client1")  # Second request
    assert throttler.request("client1") is False  # Third request should be denied

def test_quota_of_one_allows_exactly_one_request_per_window():
    throttler = Throttler(max_requests=1, time_window=10)
    assert throttler.request("client1") is True  # First request approved
    assert throttler.request("client1") is False  # Second request denied
    throttler.time_source.advance(10)  # Advance time to the next window
    assert throttler.request("client1") is True  # Third request should be approved again after waiting

def test_different_clients_isolated():
    throttler = Throttler(max_requests=1, time_window=10)
    assert throttler.request("client1") is True  # First request approved for client1
    assert throttler.request("client2") is True  # First request approved for client2

def test_denied_client_does_not_affect_others():
    throttler = Throttler(max_requests=1, time_window=10)
    assert throttler.request("client1") is True  # First request approved for client1
    assert throttler.request("client1") is False  # Second request denied for client1
    assert throttler.request("client2") is True  # First request approved for client2

def test_interleaved_requests_accounted_per_client():
    throttler = Throttler(max_requests=2, time_window=10)
    throttler.request("client1")  # Approved
    throttler.request("client2")  # Approved
    throttler.request("client1")  # Approved
    assert throttler.request("client1") is False  # Denied
    assert throttler.request("client2") is True  # Still approved

def test_request_aging_out():
    throttler = Throttler(max_requests=2, time_window=5)
    throttler.request("client1")  # Approved at t=0
    throttler.request("client1")  # Approved at t=1
    assert throttler.request("client1") is False  # Denied at t=2
    throttler.time_source.advance(5)  # Advance time to allow aging out
    assert throttler.request("client1") is True  # New request should be approved after aging out

def test_exactly_one_window_length_request_expires():
    throttler = Throttler(max_requests=1, time_window=10)
    assert throttler.request("client1") is True  # Approved at t=0
    throttler.time_source.advance(10)  # Advance time to reach boundary
    assert throttler.request("client1") is True  # New request should be approved after expiration

def test_request_just_below_window_length_counts():
    throttler = Throttler(max_requests=1, time_window=10)
    assert throttler.request("client1") is True  # Approved at t=0
    throttler.time_source.advance(9.999)  # Advance to just below the window length
    assert throttler.request("client1") is False  # Should still be denied

def test_expiry_per_request():
    throttler = Throttler(max_requests=3, time_window=10)
    throttler.request("client1")  # Approved at t=0
    throttler.time_source.advance(4)  # Advance time
    throttler.request("client1")  # Approved at t=4
    throttler.time_source.advance(6)  # Advance time to allow expiry
    assert throttler.request("client1") is True  # New request should be approved after expiry

def test_denied_request_does_not_count_against_quota():
    throttler = Throttler(max_requests=1, time_window=10)
    assert throttler.request("client1") is True  # Approved at t=0
    throttler.time_source.advance(5)  # Advance to allow denial
    assert throttler.request("client1") is False  # Denied at t=5
    throttler.time_source.advance(5)  # Advance to allow another window
    assert throttler.request("client1") is True  # Should be approved again after waiting

def test_invalid_quota_rejected():
    with pytest.raises(Exception, match=r"^max_requests must be positive$"):
        Throttler(max_requests=0, time_window=10)
    with pytest.raises(Exception, match=r"^max_requests must be positive$"):
        Throttler(max_requests=-1, time_window=10)

def test_invalid_time_window_rejected():
    with pytest.raises(Exception, match=r"^time_window must be positive$"):
        Throttler(max_requests=1, time_window=0)
    with pytest.raises(Exception, match=r"^time_window must be positive$"):
        Throttler(max_requests=1, time_window=-1)

def test_valid_time_window_fraction_accepted():
    throttler = Throttler(max_requests=1, time_window=0.5)  # Should be accepted
    assert throttler.request("client1") is True  # First request should be approved

def test_fractional_window_enforcement():
    throttler = Throttler(max_requests=1, time_window=0.5)
    assert throttler.request("client1") is True  # Approved at t=0
    throttler.time_source.advance(0.4)  # Advance to just before the window
    assert throttler.request("client1") is False  # Should be denied
    throttler.time_source.advance(0.1)  # Advance to the boundary
    assert throttler.request("client1") is True  # Should be approved again

def test_approve_after_full_window_inactivity():
    throttler = Throttler(max_requests=2, time_window=10)
    assert throttler.request("client1") is True  # Approved at t=0
    throttler.request("client1")  # Second request within quota
    throttler.time_source.advance(10)  # Advance time for a full window
    assert throttler.request("client1") is True  # Should be approved after inactivity
    assert throttler.request("client1") is True  # Should be approved again
    assert throttler.request("client1") is False  # Should be denied after exhausting quota