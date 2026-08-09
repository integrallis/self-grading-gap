import pytest
from solution import Throttler  # Assuming the class to be tested is called Throttler

class FakeClock:
    def __init__(self):
        self.time = 0

    def advance(self, seconds):
        self.time += seconds

    def current_time(self):
        return self.time


def test_first_request_approved():
    clock = FakeClock()
    throttler = Throttler(max_requests=1, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # First request should be approved


def test_within_quota_requests_approved():
    clock = FakeClock()
    throttler = Throttler(max_requests=3, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # First request
    assert throttler.request("client1") == True  # Second request
    assert throttler.request("client1") == True  # Third request


def test_exceeding_quota_request_denied():
    clock = FakeClock()
    throttler = Throttler(max_requests=2, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == False  # Denied


def test_quota_of_one_allows_one_request_per_window():
    clock = FakeClock()
    throttler = Throttler(max_requests=1, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == False  # Denied
    clock.advance(10)  # Advance time to allow new window
    assert throttler.request("client1") == True  # Approved again after 10 seconds


def test_different_clients_isolated():
    clock = FakeClock()
    throttler = Throttler(max_requests=2, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # Approved for client1
    assert throttler.request("client2") == True  # Approved for client2
    assert throttler.request("client1") == True  # Approved for client1
    assert throttler.request("client2") == True  # Approved for client2
    assert throttler.request("client1") == False  # Denied for client1


def test_interleaved_traffic_accounted_per_client():
    clock = FakeClock()
    throttler = Throttler(max_requests=2, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # client1 approved
    assert throttler.request("client2") == True  # client2 approved
    assert throttler.request("client1") == True  # client1 approved
    assert throttler.request("client2") == True  # client2 approved
    assert throttler.request("client2") == False  # client2 denied


def test_requests_older_than_window_do_not_count():
    clock = FakeClock()
    throttler = Throttler(max_requests=2, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == True  # Approved
    clock.advance(10)  # Advance time
    assert throttler.request("client1") == True  # Approved again after 10 seconds


def test_request_aged_exactly_one_window_length_no_longer_counts():
    clock = FakeClock()
    throttler = Throttler(max_requests=2, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == True  # Approved
    clock.advance(10)  # Advance time
    assert throttler.request("client1") == True  # Approved again after exactly 10 seconds


def test_request_aged_less_than_one_window_length_counts():
    clock = FakeClock()
    throttler = Throttler(max_requests=2, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == True  # Approved
    clock.advance(9.999)  # Advance time to just below 10 seconds
    assert throttler.request("client1") == False  # Denied (still within the window)


def test_expiry_per_request_not_periodic_reset():
    clock = FakeClock()
    throttler = Throttler(max_requests=3, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == False  # Denied
    clock.advance(10)  # Advance time
    assert throttler.request("client1") == True  # Approved (one slot freed)


def test_full_window_of_inactivity_resets_quota():
    clock = FakeClock()
    throttler = Throttler(max_requests=2, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == True  # Approved
    clock.advance(10)  # Advance time
    assert throttler.request("client1") == True  # Approved after full inactivity period


def test_denied_requests_do_not_consume_quota():
    clock = FakeClock()
    throttler = Throttler(max_requests=1, time_window=10, time_source=clock)
    assert throttler.request("client1") == True  # Approved
    assert throttler.request("client1") == False  # Denied
    clock.advance(10)  # Advance time
    assert throttler.request("client1") == True  # Approved again


def test_quota_below_one_rejected():
    with pytest.raises(Exception) as exc:
        Throttler(max_requests=0, time_window=10, time_source=FakeClock())
    assert str(exc.value) == "max_requests must be positive"

    with pytest.raises(Exception) as exc:
        Throttler(max_requests=-1, time_window=10, time_source=FakeClock())
    assert str(exc.value) == "max_requests must be positive"


def test_zero_or_negative_window_length_rejected():
    with pytest.raises(Exception) as exc:
        Throttler(max_requests=1, time_window=0, time_source=FakeClock())
    assert str(exc.value) == "time_window must be positive"
        
    with pytest.raises(Exception) as exc:
        Throttler(max_requests=1, time_window=-1, time_source=FakeClock())
    assert str(exc.value) == "time_window must be positive"


def test_positive_window_length_accepted():
    try:
        Throttler(max_requests=1, time_window=0.5, time_source=FakeClock())  # Accepts fractions of a second
    except Exception:
        pytest.fail("Positive window length should be accepted")


def test_fractional_window_enforcement():
    clock = FakeClock()
    throttler = Throttler(max_requests=1, time_window=0.5, time_source=clock)
    assert throttler.request("client1") == True  # Approved at t=0
    clock.advance(0.49)  # Advance time to just below 0.5 seconds
    assert throttler.request("client1") == False  # Denied at t=0.49
    clock.advance(0.01)  # Advance time to reach 0.5 seconds
    assert throttler.request("client1") == True  # Approved again at t=0.5