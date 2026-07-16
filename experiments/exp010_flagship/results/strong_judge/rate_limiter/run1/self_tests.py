import pytest
from solution import request_throttler

class FakeClock:
    def __init__(self):
        self.current_time = 0

    def advance(self, seconds):
        self.current_time += seconds
        return self.current_time

def test_first_request_approved():
    clock = FakeClock()
    assert request_throttler("client1", 1, 10, clock.current_time) == True  # First request is always approved

def test_within_quota_requests_approved():
    clock = FakeClock()
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # First request approved
    clock.advance(1)
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Second request approved within quota

def test_exceeding_quota_requests_denied():
    clock = FakeClock()
    assert request_throttler("client1", 1, 10, clock.current_time) == True  # First request approved
    clock.advance(1)
    assert request_throttler("client1", 1, 10, clock.current_time) == False  # Second request denied (exceeds quota)

def test_quota_of_one_only_one_request_approved():
    clock = FakeClock()
    assert request_throttler("client1", 1, 10, clock.current_time) == True  # First request approved
    clock.advance(1)
    assert request_throttler("client1", 1, 10, clock.current_time) == False  # Second request denied (exceeds quota)
    clock.advance(10)
    assert request_throttler("client1", 1, 10, clock.current_time) == True  # Request after window is free

def test_different_clients_are_isolated():
    clock = FakeClock()
    assert request_throttler("client1", 1, 10, clock.current_time) == True  # Client1 first request approved
    clock.advance(1)
    assert request_throttler("client2", 1, 10, clock.current_time) == True  # Client2 first request approved
    assert request_throttler("client1", 1, 10, clock.current_time) == False  # Client1 denied
    assert request_throttler("client2", 1, 10, clock.current_time) == True  # Client2 still approved

def test_interleaved_requests_accounted_per_client():
    clock = FakeClock()
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Client1 first request approved
    clock.advance(1)
    assert request_throttler("client2", 2, 10, clock.current_time) == True  # Client2 first request approved
    clock.advance(1)
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Client1 second request approved
    clock.advance(1)
    assert request_throttler("client2", 2, 10, clock.current_time) == True  # Client2 second request approved
    clock.advance(1)
    assert request_throttler("client1", 2, 10, clock.current_time) == False  # Client1 denied (exceeds quota)

def test_requests_older_than_window_no_longer_count():
    clock = FakeClock()
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Approved at 0
    clock.advance(5)
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Approved at 5
    clock.advance(6)
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Approved at 11, oldest request at 0 ages out

def test_request_aged_exactly_one_window_length_no_longer_count():
    clock = FakeClock()
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Approved at 0
    clock.advance(10)
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Approved at 10, oldest request at 0 ages out
    clock.advance(1)
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Approved at 11, 0 request ages out

def test_request_aged_less_than_one_window_length_still_count():
    clock = FakeClock()
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Approved at 0
    clock.advance(9.999)
    assert request_throttler("client1", 2, 10, clock.current_time) == False  # Denied at 9.999 (still within window)
    clock.advance(0.001)
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Request at 10 approved (0 ages out)

def test_expiry_is_per_request_not_periodic_reset():
    clock = FakeClock()
    assert request_throttler("client1", 3, 10, clock.current_time) == True  # Approved at 0
    clock.advance(4)
    assert request_throttler("client1", 3, 10, clock.current_time) == True  # Approved at 4
    clock.advance(4)
    assert request_throttler("client1", 3, 10, clock.current_time) == False  # Denied at 8 (0, 4 still count)
    clock.advance(2)
    assert request_throttler("client1", 3, 10, clock.current_time) == True  # Approved at 10 (0 ages out)

def test_full_window_of_inactivity_all_quota_available_again():
    clock = FakeClock()
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Approved at 0
    clock.advance(11)
    assert request_throttler("client1", 2, 10, clock.current_time) == True  # Approved at 11 (after full window)

def test_denied_requests_consume_no_quota():
    clock = FakeClock()
    assert request_throttler("client1", 1, 10, clock.current_time) == True  # Approved at 0
    clock.advance(5)
    assert request_throttler("client1", 1, 10, clock.current_time) == False  # Denied at 5
    clock.advance(5)
    assert request_throttler("client1", 1, 10, clock.current_time) == True  # Approved again at 10 (denied does not count)

def test_quota_below_one_rejected():
    clock = FakeClock()
    with pytest.raises(Exception, match="^max_requests must be positive$"):
        request_throttler("client1", 0, 10, clock.current_time)

def test_zero_or_negative_window_length_rejected():
    clock = FakeClock()
    with pytest.raises(Exception, match="^time_window must be positive$"):
        request_throttler("client1", 1, 0, clock.current_time)
    with pytest.raises(Exception, match="^time_window must be positive$"):
        request_throttler("client1", 1, -1, clock.current_time)

def test_positive_window_length_accepted():
    clock = FakeClock()
    assert request_throttler("client1", 1, 0.1, clock.current_time) == True  # Accepted with a fractional window length
    assert request_throttler("client1", 1, 10, clock.current_time) == True  # Accepted with a positive window length

def test_request_aged_within_epsilon_still_counts():
    clock = FakeClock()
    assert request_throttler("client1", 1, 10, clock.current_time) == True  # Approved at 0
    clock.advance(0.099)
    assert request_throttler("client1", 1, 0.1, clock.current_time) == False  # Denied at 0.099 (counts)

def test_full_window_inactivity_with_multiple_quota():
    clock = FakeClock()
    assert request_throttler("client1", 3, 10, clock.current_time) == True  # Approved at 0
    clock.advance(5)
    assert request_throttler("client1", 3, 10, clock.current_time) == True  # Approved at 5
    clock.advance(4)
    assert request_throttler("client1", 3, 10, clock.current_time) == True  # Approved at 9
    clock.advance(1)
    assert request_throttler("client1", 3, 10, clock.current_time) == False  # Denied at 10 (all counts)
    clock.advance(10)
    assert request_throttler("client1", 3, 10, clock.current_time) == True  # Approved at 20 (after full window)