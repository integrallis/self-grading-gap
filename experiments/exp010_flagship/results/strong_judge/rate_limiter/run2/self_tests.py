import pytest
from solution import Throttle

class FakeTimeSource:
    def __init__(self):
        self.current_time = 0

    def advance(self, seconds):
        self.current_time += seconds
        return self.current_time

    def now(self):
        return self.current_time

def test_first_request_approved():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=3, time_window=10, time_source=time_source)
    assert throttle.request('client1') == True  # First request is approved

def test_within_quota_requests_approved():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=3, time_window=10, time_source=time_source)
    throttle.request('client1')  # First request
    assert throttle.request('client1') == True  # Within quota
    assert throttle.request('client1') == True  # Within quota

def test_exceeding_quota_request_denied():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=3, time_window=10, time_source=time_source)
    throttle.request('client1')  # First request
    throttle.request('client1')  # Second request
    throttle.request('client1')  # Third request
    assert throttle.request('client1') == False  # Exceeds quota

def test_quota_of_one_request_per_window():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=1, time_window=10, time_source=time_source)
    assert throttle.request('client1') == True  # Approved
    assert throttle.request('client1') == False  # Denied
    time_source.advance(10)  # Advance to exactly time 10
    assert throttle.request('client1') == True  # Approved again after window

def test_different_clients_isolation():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=3, time_window=10, time_source=time_source)
    assert throttle.request('client1') == True  # client1 approved
    assert throttle.request('client2') == True  # client2 approved
    throttle.request('client1')  # client1 within quota
    throttle.request('client1')  # client1 within quota
    assert throttle.request('client1') == False  # client1 exceeds quota
    assert throttle.request('client2') == True  # client2 still approved

def test_interleaved_traffic_accounted_per_client():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=2, time_window=10, time_source=time_source)
    assert throttle.request('client1') == True  # client1 approved
    assert throttle.request('client2') == True  # client2 approved
    assert throttle.request('client1') == True  # client1 within quota
    assert throttle.request('client2') == True  # client2 within quota
    assert throttle.request('client1') == False  # client1 exceeds quota
    assert throttle.request('client2') == False  # client2 exceeds quota

def test_requests_aging_out():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=2, time_window=10, time_source=time_source)
    throttle.request('client1')  # Approved at t=0
    throttle.advance(2)  # Advance time to 2
    throttle.request('client1')  # Approved at t=2
    assert throttle.request('client1') == False  # Denied (still counts)
    throttle.advance(8)  # Advance time to 10
    assert throttle.request('client1') == True  # Approved (one request ages out)

def test_request_aged_exactly_one_window_length_no_longer_counts():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=2, time_window=10, time_source=time_source)
    throttle.request('client1')  # Approved at t=0
    throttle.advance(5)  # Advance time to 5
    throttle.request('client1')  # Approved at t=5
    throttle.advance(5)  # Advance time to 10
    assert throttle.request('client1') == True  # Aged out at t=10

def test_request_aged_less_than_one_window_length_still_counts():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=2, time_window=10, time_source=time_source)
    throttle.request('client1')  # Approved at t=0
    throttle.advance(5)  # Advance time to 5
    throttle.request('client1')  # Approved at t=5
    throttle.advance(4.999)  # Advance time to 9.999
    assert throttle.request('client1') == False  # Denied (still counts)

def test_expiry_per_request():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=3, time_window=10, time_source=time_source)
    throttle.request('client1')  # Approved at t=0
    throttle.advance(1)  # Advance time to 1
    throttle.request('client1')  # Approved at t=1
    throttle.advance(1)  # Advance time to 2
    throttle.request('client1')  # Approved at t=2
    assert throttle.request('client1') == False  # Denied
    throttle.advance(10)  # Wait for more than the window
    assert throttle.request('client1') == True  # Approved again after inactivity

def test_denied_requests_do_not_consume_quota():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=1, time_window=10, time_source=time_source)
    assert throttle.request('client1') == True  # Approved
    assert throttle.request('client1') == False  # Denied
    throttle.advance(10)  # Advance time to 10
    assert throttle.request('client1') == True  # Approved again

def test_invalid_quota_below_one():
    with pytest.raises(ValueError) as excinfo:
        Throttle(max_requests=0, time_window=10, time_source=FakeTimeSource())
    assert str(excinfo.value) == "max_requests must be positive"

def test_invalid_time_window_zero_or_negative():
    with pytest.raises(ValueError) as excinfo:
        Throttle(max_requests=1, time_window=0, time_source=FakeTimeSource())
    assert str(excinfo.value) == "time_window must be positive"
    
    with pytest.raises(ValueError) as excinfo:
        Throttle(max_requests=1, time_window=-1, time_source=FakeTimeSource())
    assert str(excinfo.value) == "time_window must be positive"

def test_valid_time_window_fraction():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=1, time_window=0.5, time_source=time_source)  # Accepts fraction
    assert throttle.request('client1') == True  # Approved
    throttle.advance(0.5)  # Advance time to 0.5
    assert throttle.request('client1') == False  # Denied (still within window)
    throttle.advance(0.5)  # Advance time to 1
    assert throttle.request('client1') == True  # Approved (after window)

def test_full_inactivity_resets_quota():
    time_source = FakeTimeSource()
    throttle = Throttle(max_requests=2, time_window=10, time_source=time_source)
    throttle.request('client1')  # Approved
    throttle.request('client1')  # Approved
    assert throttle.request('client1') == False  # Denied
    throttle.advance(10)  # Wait for exactly 10 seconds (full window of inactivity)
    assert throttle.request('client1') == True  # Approved again after inactivity

def test_invalid_quota_negative():
    with pytest.raises(ValueError) as excinfo:
        Throttle(max_requests=-1, time_window=10, time_source=FakeTimeSource())
    assert str(excinfo.value) == "max_requests must be positive"