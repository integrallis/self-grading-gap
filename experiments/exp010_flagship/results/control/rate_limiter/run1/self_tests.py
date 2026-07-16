from solution import request_throttle

def test_first_request_approved():
    assert request_throttle("client1", 1, 10, 0) == True  # First request should be approved

def test_subsequent_requests_within_quota():
    assert request_throttle("client1", 1, 10, 0) == True  # Approved
    assert request_throttle("client1", 1, 10, 5) == True  # Approved within quota

def test_exceeding_quota_denied():
    assert request_throttle("client1", 1, 10, 0) == True  # Approved
    assert request_throttle("client1", 1, 10, 5) == True  # Approved
    assert request_throttle("client1", 1, 10, 6) == False # Denied, exceeds quota

def test_quota_of_one():
    assert request_throttle("client1", 1, 10, 0) == True  # Approved
    assert request_throttle("client1", 1, 10, 5) == False # Denied
    assert request_throttle("client1", 1, 10, 10) == True  # Approved after window

def test_clients_isolated_from_each_other():
    assert request_throttle("client1", 1, 10, 0) == True  # Client 1 approved
    assert request_throttle("client2", 1, 10, 0) == True  # Client 2 approved
    assert request_throttle("client1", 1, 10, 5) == True  # Client 1 approved again
    assert request_throttle("client2", 1, 10, 5) == True  # Client 2 approved again
    assert request_throttle("client1", 1, 10, 6) == False # Client 1 denied

def test_interleaved_traffic_accounted_per_client():
    assert request_throttle("client1", 2, 10, 0) == True  # Client 1 approved
    assert request_throttle("client2", 2, 10, 0) == True  # Client 2 approved
    assert request_throttle("client1", 2, 10, 5) == True  # Client 1 approved
    assert request_throttle("client2", 2, 10, 5) == True  # Client 2 approved
    assert request_throttle("client1", 2, 10, 6) == False # Client 1 denied

def test_requests_older_than_window_no_longer_count():
    assert request_throttle("client1", 1, 10, 0) == True  # Approved
    assert request_throttle("client1", 1, 10, 5) == True  # Approved
    assert request_throttle("client1", 1, 10, 12) == True  # Approved after expiry

def test_requests_aged_exactly_one_window_length_no_longer_count():
    assert request_throttle("client1", 1, 10, 0) == True  # Approved
    assert request_throttle("client1", 1, 10, 10) == True  # Approved at edge
    assert request_throttle("client1", 1, 10, 11) == False # Denied immediately after

def test_requests_aged_less_than_one_window_length_still_count():
    assert request_throttle("client1", 1, 10, 0) == True  # Approved
    assert request_throttle("client1", 1, 10, 9) == True  # Approved
    assert request_throttle("client1", 1, 10, 10) == True  # Approved
    assert request_throttle("client1", 1, 10, 11) == False # Denied

def test_expiry_per_request_not_periodic_reset():
    assert request_throttle("client1", 3, 10, 0) == True  # Approved
    assert request_throttle("client1", 3, 10, 4) == True  # Approved
    assert request_throttle("client1", 3, 10, 8) == True  # Approved
    assert request_throttle("client1", 3, 10, 9) == False # Denied
    assert request_throttle("client1", 3, 10, 10) == True  # Approved after expiry

def test_full_window_of_inactivity_resets_quota():
    assert request_throttle("client1", 2, 10, 0) == True  # Approved
    assert request_throttle("client1", 2, 10, 5) == True  # Approved
    assert request_throttle("client1", 2, 10, 11) == True  # Approved after inactivity

def test_denied_requests_do_not_consume_quota():
    assert request_throttle("client1", 1, 10, 0) == True  # Approved
    assert request_throttle("client1", 1, 10, 5) == False # Denied
    assert request_throttle("client1", 1, 10, 10) == True  # Approved after window

def test_invalid_quota_below_one():
    try:
        request_throttle("client1", 0, 10, 0)
    except ValueError as e:
        assert str(e) == "max_requests must be positive"

def test_invalid_window_length_zero_or_negative():
    try:
        request_throttle("client1", 1, 0, 0)
    except ValueError as e:
        assert str(e) == "time_window must be positive"

    try:
        request_throttle("client1", 1, -1, 0)
    except ValueError as e:
        assert str(e) == "time_window must be positive"

def test_valid_fractional_window_length():
    assert request_throttle("client1", 1, 0.5, 0) == True  # Approved
    assert request_throttle("client1", 1, 0.5, 0.3) == True  # Approved
    assert request_throttle("client1", 1, 0.5, 0.6) == False # Denied