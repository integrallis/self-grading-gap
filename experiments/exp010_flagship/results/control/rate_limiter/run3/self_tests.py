from solution import SlidingWindowThrottler

def test_first_request_approved():
    throttler = SlidingWindowThrottler(max_requests=2, time_window=10)
    assert throttler.request("client1", 0) == True  # First request, should be approved

def test_subsequent_requests_within_quota_approved():
    throttler = SlidingWindowThrottler(max_requests=2, time_window=10)
    throttler.request("client1", 0)  # Approve first request
    assert throttler.request("client1", 5) == True  # Second request, should be approved

def test_request_exceeding_quota_denied():
    throttler = SlidingWindowThrottler(max_requests=2, time_window=10)
    throttler.request("client1", 0)  # Approve first request
    throttler.request("client1", 5)  # Approve second request
    assert throttler.request("client1", 6) == False  # Third request, should be denied

def test_quota_of_one_allows_one_request_per_window():
    throttler = SlidingWindowThrottler(max_requests=1, time_window=10)
    assert throttler.request("client1", 0) == True  # Approve first request
    assert throttler.request("client1", 5) == False  # Deny second request within the same window
    assert throttler.request("client1", 10) == True  # Approve request after window

def test_client_exceeding_quota_does_not_affect_other_clients():
    throttler = SlidingWindowThrottler(max_requests=2, time_window=10)
    throttler.request("client1", 0)  # Approve first request for client1
    throttler.request("client1", 5)  # Approve second request for client1
    assert throttler.request("client2", 6) == True  # client2 should be approved

def test_interleaved_traffic_accounted_per_client():
    throttler = SlidingWindowThrottler(max_requests=2, time_window=10)
    throttler.request("client1", 0)  # Approve first request for client1
    throttler.request("client2", 1)  # Approve first request for client2
    throttler.request("client1", 5)  # Approve second request for client1
    assert throttler.request("client2", 6) == True  # client2 should still be approved

def test_old_requests_no_longer_count_against_quota():
    throttler = SlidingWindowThrottler(max_requests=2, time_window=10)
    throttler.request("client1", 0)  # Approve first request
    throttler.request("client1", 5)  # Approve second request
    assert throttler.request("client1", 11) == True  # Old requests should not count, approve new request

def test_request_aged_exactly_one_window_length_no_longer_count():
    throttler = SlidingWindowThrottler(max_requests=2, time_window=10)
    throttler.request("client1", 0)  # Approve first request
    throttler.request("client1", 5)  # Approve second request
    assert throttler.request("client1", 10) == True  # Request at 10 should be approved after 10 seconds

def test_request_aged_less_than_one_window_length_still_counts():
    throttler = SlidingWindowThrottler(max_requests=2, time_window=10)
    throttler.request("client1", 0)  # Approve first request
    throttler.request("client1", 5)  # Approve second request
    assert throttler.request("client1", 9) == False  # Request at 9 should be denied

def test_expiry_is_per_request_not_periodic_reset():
    throttler = SlidingWindowThrottler(max_requests=3, time_window=10)
    throttler.request("client1", 0)  # Approve at 0
    throttler.request("client1", 4)  # Approve at 4
    throttler.request("client1", 8)  # Approve at 8
    assert throttler.request("client1", 9) == False  # Denied at 9
    assert throttler.request("client1", 10) == True  # Approved at 10, one slot freed

def test_full_window_of_inactivity_resets_quota():
    throttler = SlidingWindowThrottler(max_requests=2, time_window=10)
    throttler.request("client1", 0)  # Approve first request
    throttler.request("client1", 5)  # Approve second request
    assert throttler.request("client1", 15) == True  # Approved after full window of inactivity

def test_denied_request_not_recorded_against_window():
    throttler = SlidingWindowThrottler(max_requests=1, time_window=10)
    throttler.request("client1", 0)  # Approve first request
    throttler.request("client1", 5)  # Deny second request
    assert throttler.request("client1", 10) == True  # Should be approved again after the window

def test_invalid_quota_rejected():
    with pytest.raises(ValueError, match="max_requests must be positive"):
        SlidingWindowThrottler(max_requests=0, time_window=10)

def test_invalid_time_window_rejected():
    with pytest.raises(ValueError, match="time_window must be positive"):
        SlidingWindowThrottler(max_requests=1, time_window=0)