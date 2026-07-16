import time
import pytest
from solution import CircuitBreaker  # Assuming the class is named CircuitBreaker

def test_initial_state():
    breaker = CircuitBreaker()
    assert breaker.state == 'closed'  # AC-1.1

def test_successful_call_when_closed():
    breaker = CircuitBreaker()
    result = breaker.call(lambda: "success")  # AC-1.2
    assert result == "success"

def test_failing_call_when_closed():
    breaker = CircuitBreaker()
    with pytest.raises(Exception):  # AC-1.3
        breaker.call(lambda: 1 / 0)

def test_consecutive_failures_below_threshold():
    breaker = CircuitBreaker()
    try:
        breaker.call(lambda: 1 / 0)  # First failure
    except Exception:
        pass
    try:
        breaker.call(lambda: 1 / 0)  # Second failure
    except Exception:
        pass
    assert breaker.state == 'closed'  # AC-1.4

def test_success_resets_failure_count():
    breaker = CircuitBreaker()
    try:
        breaker.call(lambda: 1 / 0)  # First failure
    except Exception:
        pass
    result = breaker.call(lambda: "success")  # AC-1.5
    assert result == "success"
    try:
        breaker.call(lambda: 1 / 0)  # New failure
    except Exception:
        pass
    assert breaker.state == 'closed'

def test_opens_circuit_after_consecutive_failures():
    breaker = CircuitBreaker()
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Three failures
        except Exception:
            pass
    assert breaker.state == 'open'  # AC-2.1

def test_rejects_calls_when_open():
    breaker = CircuitBreaker()
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Three failures
        except Exception:
            pass
    with pytest.raises(Exception) as excinfo:  # AC-2.2
        breaker.call(lambda: "should not be called")
    assert str(excinfo.value) == "circuit breaker is open"

def test_calls_rejected_during_reset_timeout():
    breaker = CircuitBreaker()
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Three failures
        except Exception:
            pass
    time.sleep(30)  # Wait for reset timeout
    with pytest.raises(Exception) as excinfo:  # AC-2.3
        breaker.call(lambda: "should not be called")
    assert str(excinfo.value) == "circuit breaker is open"

def test_probe_call_success_after_timeout():
    breaker = CircuitBreaker()
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Three failures
        except Exception:
            pass
    time.sleep(30)  # Wait for reset timeout
    result = breaker.call(lambda: "success")  # AC-3.2
    assert result == "success"
    assert breaker.state == 'closed'

def test_probe_call_failure_after_timeout():
    breaker = CircuitBreaker()
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Three failures
        except Exception:
            pass
    time.sleep(30)  # Wait for reset timeout
    with pytest.raises(Exception) as excinfo:  # AC-3.3
        breaker.call(lambda: 1 / 0)
    assert str(excinfo.value) == "circuit breaker is open"
    assert breaker.state == 'open'  # AC-3.3

def test_failed_probe_resets_timeout():
    breaker = CircuitBreaker()
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Three failures
        except Exception:
            pass
    time.sleep(30)  # Wait for reset timeout
    with pytest.raises(Exception):
        breaker.call(lambda: 1 / 0)  # First probe fails
    time.sleep(30)  # Wait for another timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    assert str(excinfo.value) == "circuit breaker is open"

def test_custom_failure_threshold():
    breaker = CircuitBreaker(failure_threshold=1)
    try:
        breaker.call(lambda: 1 / 0)  # Single failure opens circuit
    except Exception:
        pass
    assert breaker.state == 'open'  # AC-4.1

def test_custom_reset_timeout():
    breaker = CircuitBreaker(reset_timeout=10)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # Three failures
        except Exception:
            pass
    time.sleep(10)  # Wait for reset timeout
    result = breaker.call(lambda: "success")  # AC-4.2
    assert result == "success"