import pytest
from solution import throttler_function  # Replace with the actual function name

def test_first_request_approved():
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1") == True  # First request should be approved

def test_within_quota_requests_approved():
    throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1")  # Approve first request
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1") == True  # Second request within quota should be approved

def test_exceeding_quota_request_denied():
    throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1")  # Approve first request
    throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1")  # Approve second request
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1") == False  # Third request exceeds the quota and should be denied

def test_single_request_quota():
    assert throttler_function(max_requests=1, time_window=10, time_source=lambda: 0, client="client1") == True  # First request should be approved
    assert throttler_function(max_requests=1, time_window=10, time_source=lambda: 0, client="client1") == False  # Second request should be denied

def test_different_clients_isolation():
    throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1")  # Approve client1's first request
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client2") == True  # Approve client2's first request
    throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1")  # Approve client1's second request
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1") == False  # client1's third request should be denied
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client2") == True  # client2's second request should be approved

def test_interleaved_traffic_accounting():
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1") == True  # Approve client1's first request
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client2") == True  # Approve client2's first request
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1") == True  # Approve client1's second request
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client2") == True  # Approve client2's second request
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1") == False  # client1's third request should be denied
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client2") == False  # client2's third request should also be denied

def test_requests_aging_out():
    throttler_function(max_requests=2, time_window=10, time_source=lambda: 0, client="client1")  # Approve first request
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 5, client="client1") == True  # Approve second request
    assert throttler_function(max_requests=2, time_window=10, time_source=lambda: 11, client="client1") == True  # Should now be approved again

def test_boundary_condition():
    assert throttler_function(max_requests=3, time_window=10, time_source=lambda: 0, client="client1") == True  # Approve at time 0
    assert throttler_function(max_requests=3, time_window=10, time_source=lambda: 4, client="client1") == True  # Approve at time 4
    assert throttler_function(max_requests=3, time_window=10, time_source=lambda: 8, client="client1") == True  # Approve at time 8
    assert throttler_function(max_requests=3, time_window=10, time_source=lambda: 9, client="client1") == False  # Should be denied at time 9
    assert throttler_function(max_requests=3, time_window=10, time_source=lambda: 10, client="client1") == True  # Should be approved at time 10
    assert throttler_function(max_requests=3, time_window=10, time_source=lambda: 10, client="client1") == False  # New request at time 10 should be denied

def test_denied_requests_do_not_consume_quota():
    assert throttler_function(max_requests=1, time_window=10, time_source=lambda: 0, client="client1") == True  # Approve first request
    assert throttler_function(max_requests=1, time_window=10, time_source=lambda: 0, client="client1") == False  # Deny second request
    assert throttler_function(max_requests=1, time_window=10, time_source=lambda: 10, client="client1") == True  # Should be approved again after window reset

def test_invalid_quota():
    with pytest.raises(Exception) as excinfo:
        throttler_function(max_requests=0, time_window=10, time_source=lambda: 0, client="client1")
    assert str(excinfo.value) == "max_requests must be positive"
    
    with pytest.raises(Exception) as excinfo:
        throttler_function(max_requests=-1, time_window=10, time_source=lambda: 0, client="client1")
    assert str(excinfo.value) == "max_requests must be positive"

def test_invalid_time_window():
    with pytest.raises(Exception) as excinfo:
        throttler_function(max_requests=1, time_window=0, time_source=lambda: 0, client="client1")
    assert str(excinfo.value) == "time_window must be positive"
    
    with pytest.raises(Exception) as excinfo:
        throttler_function(max_requests=1, time_window=-10, time_source=lambda: 0, client="client1")
    assert str(excinfo.value) == "time_window must be positive"

def test_fractional_time_window():
    assert throttler_function(max_requests=1, time_window=0.5, time_source=lambda: 0, client="client1") == True  # First request should be approved
    assert throttler_function(max_requests=1, time_window=0.5, time_source=lambda: 0.6, client="client1") == True  # Should be approved again after window resets