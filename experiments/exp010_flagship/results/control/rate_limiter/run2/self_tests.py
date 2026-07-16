from solution import Throttle

def test_first_request_approved():
    throttle = Throttle(max_requests=3, time_window=10)
    assert throttle.request("client1", 0) == True  # First request approved

def test_second_request_approved_within_quota():
    throttle = Throttle(max_requests=3, time_window=10)
    throttle.request("client1", 0)
    assert throttle.request("client1", 2) == True  # Second request approved

def test_request_exceeds_quota():
    throttle = Throttle(max_requests=2, time_window=10)
    throttle.request("client1", 0)
    throttle.request("client1", 2)
    assert throttle.request("client1", 4) == False  # Third request denied

def test_one_request_approved_per_window_with_quota_one():
    throttle = Throttle(max_requests=1, time_window=10)
    assert throttle.request("client1", 0) == True  # First request approved
    assert throttle.request("client1", 5) == False  # Second request denied

def test_client_exceeding_quota_does_not_affect_other_clients():
    throttle = Throttle(max_requests=1, time_window=10)
    assert throttle.request("client1", 0) == True  # client1 approved
    assert throttle.request("client1", 5) == False  # client1 denied
    assert throttle.request("client2", 2) == True  # client2 approved

def test_interleaved_requests_accounted_per_client():
    throttle = Throttle(max_requests=2, time_window=10)
    assert throttle.request("client1", 0) == True  # client1 approved
    assert throttle.request("client2", 1) == True  # client2 approved
    assert throttle.request("client1", 2) == True  # client1 approved
    assert throttle.request("client2", 3) == False  # client2 denied

def test_request_ages_out_and_is_reapproved():
    throttle = Throttle(max_requests=2, time_window=10)
    throttle.request("client1", 0)
    throttle.request("client1", 2)
    assert throttle.request("client1", 11) == True  # Request at second 11 approved as old requests have aged out

def test_request_aged_exactly_one_window_length_no_longer_counts():
    throttle = Throttle(max_requests=2, time_window=10)
    throttle.request("client1", 0)
    throttle.request("client1", 2)
    assert throttle.request("client1", 10) == True  # Approved again as the first request is exactly aged out

def test_request_aged_less_than_one_window_length_still_counts():
    throttle = Throttle(max_requests=2, time_window=10)
    throttle.request("client1", 0)
    throttle.request("client1", 2)
    assert throttle.request("client1", 9) == False  # Denied as the first request is still within window

def test_expiry_is_per_request():
    throttle = Throttle(max_requests=3, time_window=10)
    throttle.request("client1", 0)  # Approved
    throttle.request("client1", 4)  # Approved
    throttle.request("client1", 8)  # Approved
    assert throttle.request("client1", 9) == False  # Denied
    assert throttle.request("client1", 10) == True  # Approved again as the request at 0 has expired

def test_full_window_of_inactivity_resets_quota():
    throttle = Throttle(max_requests=1, time_window=10)
    assert throttle.request("client1", 0) == True  # Approved
    assert throttle.request("client1", 5) == False  # Denied
    assert throttle.request("client1", 11) == True  # Approved again after inactivity

def test_denied_requests_do_not_consume_quota():
    throttle = Throttle(max_requests=1, time_window=10)
    assert throttle.request("client1", 0) == True  # Approved
    assert throttle.request("client1", 5) == False  # Denied
    assert throttle.request("client1", 10) == True  # Approved again, denial does not count

def test_negative_quota_raises_error():
    try:
        Throttle(max_requests=-1, time_window=10)
    except ValueError as e:
        assert str(e) == "max_requests must be positive"

def test_zero_window_length_raises_error():
    try:
        Throttle(max_requests=1, time_window=0)
    except ValueError as e:
        assert str(e) == "time_window must be positive"

def test_negative_window_length_raises_error():
    try:
        Throttle(max_requests=1, time_window=-5)
    except ValueError as e:
        assert str(e) == "time_window must be positive"

def test_fractional_window_length_is_accepted():
    throttle = Throttle(max_requests=1, time_window=0.5)
    assert throttle.request("client1", 0) == True  # Approved
    assert throttle.request("client1", 0.3) == False  # Denied
    assert throttle.request("client1", 0.6) == True  # Approved again