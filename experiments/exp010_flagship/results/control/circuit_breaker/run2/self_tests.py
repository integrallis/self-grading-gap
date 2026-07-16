from solution import CircuitBreaker
import time
import pytest

def test_circuit_breaker_initial_state():
    breaker = CircuitBreaker()
    assert breaker.state == 'closed'  # AC-1.1

def test_circuit_breaker_pass_through_success():
    breaker = CircuitBreaker()
    result = breaker.call(lambda: "success")
    assert result == "success"  # AC-1.2

def test_circuit_breaker_pass_through_failure():
    breaker = CircuitBreaker()
    with pytest.raises(Exception):  # Assuming the underlying operation raises Exception
        breaker.call(lambda: 1 / 0)  # Simulate failure
    assert breaker.state == 'closed'  # AC-1.3

def test_circuit_breaker_consecutive_failures():
    breaker = CircuitBreaker()
    for _ in range(2):
        try:
            breaker.call(lambda: 1 / 0)  # Simulate failure
        except Exception:
            pass
    assert breaker.state == 'closed'  # AC-1.4

def test_circuit_breaker_reset_on_success():
    breaker = CircuitBreaker()
    try:
        breaker.call(lambda: 1 / 0)  # Simulate failure
    except Exception:
        pass
    result = breaker.call(lambda: "success")  # A success resets the count
    assert result == "success"  # AC-1.5
    assert breaker.state == 'closed'  # Should still be closed

def test_circuit_breaker_open_after_threshold():
    breaker = CircuitBreaker(failure_threshold=3)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Simulate failure
        except Exception:
            pass
    assert breaker.state == 'open'  # AC-2.1

def test_circuit_breaker_rejects_calls_when_open():
    breaker = CircuitBreaker(failure_threshold=3)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Simulate failure
        except Exception:
            pass
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "success")  # Should not invoke the operation
    assert str(excinfo.value) == "circuit breaker is open"  # AC-2.2

def test_circuit_breaker_rejects_for_timeout():
    breaker = CircuitBreaker(reset_timeout=1, failure_threshold=3)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Simulate failure
        except Exception:
            pass
    time.sleep(1)
    with pytest.raises(Exception):
        breaker.call(lambda: "success")  # Should still be open
    assert breaker.state == 'open'  # AC-2.3

def test_circuit_breaker_probe_success():
    breaker = CircuitBreaker(reset_timeout=1, failure_threshold=3)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Simulate failure
        except Exception:
            pass
    time.sleep(1)
    result = breaker.call(lambda: "success")  # This should succeed and close
    assert result == "success"  # AC-3.2
    assert breaker.state == 'closed'  # Circuit should close

def test_circuit_breaker_probe_failure():
    breaker = CircuitBreaker(reset_timeout=1, failure_threshold=3)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Simulate failure
        except Exception:
            pass
    time.sleep(1)
    with pytest.raises(Exception):
        breaker.call(lambda: 1 / 0)  # Probe fails
    assert breaker.state == 'open'  # Circuit should reopen after failure

def test_circuit_breaker_reset_timeout_restarts():
    breaker = CircuitBreaker(reset_timeout=1, failure_threshold=3)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Simulate failure
        except Exception:
            pass
    time.sleep(1)
    with pytest.raises(Exception):
        breaker.call(lambda: 1 / 0)  # First probe fails
    time.sleep(1)  # Wait for timeout
    with pytest.raises(Exception):
        breaker.call(lambda: 1 / 0)  # Second probe should fail
    assert breaker.state == 'open'

def test_circuit_breaker_custom_failure_threshold():
    breaker = CircuitBreaker(failure_threshold=1)  # Custom threshold of 1
    try:
        breaker.call(lambda: 1 / 0)  # Simulate failure
    except Exception:
        pass
    assert breaker.state == 'open'  # AC-4.1

def test_circuit_breaker_custom_reset_timeout():
    breaker = CircuitBreaker(reset_timeout=1, failure_threshold=3)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Simulate failure
        except Exception:
            pass
    time.sleep(1)
    result = breaker.call(lambda: "success")  # Should succeed after custom timeout
    assert result == "success"  # AC-4.2
    assert breaker.state == 'closed'