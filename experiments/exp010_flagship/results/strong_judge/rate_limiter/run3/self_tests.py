import pytest
from solution import throttle_requests

# Helper function to simulate time passing
class Clock:
    def __init__(self):
        self.current_time = 0

    def advance(self, seconds):
        self.current_time += seconds
        return self.current_time

def test_first_request_is_approved():
    clock = Clock()
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(0), client="client1") == True  # first request should be approved

def test_second_request_within_quota_is_approved():
    clock = Clock()
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(0), client="client1")  # first request
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client1") == True  # second request within quota

def test_request_exceeding_quota_is_denied():
    clock = Clock()
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(0), client="client1")  # first request
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client1")  # second request
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client1") == False  # third request exceeds quota

def test_one_request_approved_per_window_with_quota_of_one():
    clock = Clock()
    throttle_requests(max_requests=1, time_window=10, current_time=clock.advance(0), client="client1")  # first request approved
    assert throttle_requests(max_requests=1, time_window=10, current_time=clock.advance(1), client="client1") == False  # second request denied
    assert throttle_requests(max_requests=1, time_window=10, current_time=clock.advance(10), client="client1") == True  # after window, approved again

def test_client_denied_does_not_affect_another_client():
    clock = Clock()
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(0), client="client1")  # first request from client1
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client1")  # second request from client1
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client2") == True  # client2 should still be approved

def test_interleaved_traffic_accounted_per_client():
    clock = Clock()
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(0), client="client1")
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(0), client="client2")
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client1")
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client2") == True  # client2 still under quota
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client1") == False  # client1 should be denied

def test_requests_older_than_window_no_longer_count():
    clock = Clock()
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(0), client="client1")  # t=0
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client1")  # t=1
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(10), client="client1") == True  # t=11, first request ages out

def test_request_aged_exactly_one_window_length_no_longer_counts():
    clock = Clock()
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(0), client="client1")  # t=0
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client1")  # t=1
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(10), client="client1") == True  # t=10, request at 10 should count again

def test_request_aged_less_than_one_window_length_still_counts():
    clock = Clock()
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(0), client="client1")  # t=0
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client1")  # t=1
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(9), client="client1") == False  # t=9, still within the quota

def test_expiry_is_per_request_not_periodic_reset():
    clock = Clock()
    throttle_requests(max_requests=3, time_window=10, current_time=clock.advance(0), client="client1")  # t=0
    throttle_requests(max_requests=3, time_window=10, current_time=clock.advance(4), client="client1")  # t=4
    throttle_requests(max_requests=3, time_window=10, current_time=clock.advance(8), client="client1")  # t=8
    assert throttle_requests(max_requests=3, time_window=10, current_time=clock.advance(9), client="client1") == False  # t=9, should be denied
    assert throttle_requests(max_requests=3, time_window=10, current_time=clock.advance(10), client="client1") == True  # t=10, request at 10 frees one slot

def test_full_window_of_inactivity_resets_quota():
    clock = Clock()
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(0), client="client1")  # t=0
    throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(1), client="client1")  # t=1
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(15), client="client1") == True  # t=15, after inactivity, approved again
    assert throttle_requests(max_requests=2, time_window=10, current_time=clock.advance(16), client="client1") == False  # t=16, should be denied if all used

def test_denied_request_consumes_no_quota():
    clock = Clock()
    assert throttle_requests(max_requests=1, time_window=10, current_time=clock.advance(0), client="client1") == True  # first request approved
    assert throttle_requests(max_requests=1, time_window=10, current_time=clock.advance(1), client="client1") == False  # second request denied
    assert throttle_requests(max_requests=1, time_window=10, current_time=clock.advance(10), client="client1") == True  # should be approved again after the window

def test_quota_below_one_rejected():
    with pytest.raises(ValueError) as exc_info:
        throttle_requests(max_requests=0, time_window=10, current_time=0, client="client1")
    assert str(exc_info.value) == "max_requests must be positive"

def test_zero_or_negative_window_length_rejected():
    with pytest.raises(ValueError) as exc_info:
        throttle_requests(max_requests=1, time_window=0, current_time=0, client="client1")
    assert str(exc_info.value) == "time_window must be positive"
    
    with pytest.raises(ValueError) as exc_info:
        throttle_requests(max_requests=1, time_window=-5, current_time=0, client="client1")
    assert str(exc_info.value) == "time_window must be positive"

def test_positive_window_length_accepted():
    throttle_requests(max_requests=1, time_window=1.5, current_time=0, client="client1")  # fraction of a second accepted
    assert throttle_requests(max_requests=1, time_window=1.5, current_time=0, client="client1") == True  # first request approved

def test_fractional_window_enforcement():
    clock = Clock()
    assert throttle_requests(max_requests=1, time_window=1.5, current_time=clock.advance(0), client="client1") == True  # approved at t=0
    assert throttle_requests(max_requests=1, time_window=1.5, current_time=clock.advance(1.49), client="client1") == False  # denied at t=1.49
    assert throttle_requests(max_requests=1, time_window=1.5, current_time=clock.advance(1.5), client="client1") == True  # approved at t=1.5 after aging out