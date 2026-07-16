import pytest
from solution import *

class FakeClock:
    def __init__(self):
        self.current_time = 0

    def advance(self, seconds):
        self.current_time += seconds

    def time(self):
        return self.current_time

def test_initial_state_is_closed():
    breaker = CircuitBreaker(clock=FakeClock())
    # Initial state should be closed
    assert breaker.state() == "closed"  # AC-1.1

def test_successful_call_returns_result():
    breaker = CircuitBreaker(clock=FakeClock())
    result = breaker.call(lambda: "success")
    # A successful call should return the result unchanged
    assert result == "success"  # AC-1.2

def test_failing_call_propagates_error():
    breaker = CircuitBreaker(clock=FakeClock())
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)
    # A failing call should propagate the error
    assert str(excinfo.value) == "division by zero"  # AC-1.3

def test_consecutive_failures_below_threshold():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(2):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    # The breaker should remain closed after 2 failures
    assert breaker.state() == "closed"  # AC-1.4

def test_success_resets_failure_count():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    try:
        breaker.call(lambda: 1 / 0)
    except Exception:
        pass
    breaker.call(lambda: "success")  # resets failure count
    for _ in range(2):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    # The breaker should remain closed after a success
    assert breaker.state() == "closed"  # AC-1.5

def test_open_circuit_after_threshold_reached():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    # After 3 failures, the circuit should open
    assert breaker.state() == "open"  # AC-2.1

def test_open_circuit_rejects_calls():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    # Calls should be rejected with the correct message
    assert str(excinfo.value) == "circuit breaker is open"  # AC-2.2

def test_rejection_just_before_reset_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(29.9)  # advance just before timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    # Call should still be rejected just before timeout
    assert str(excinfo.value) == "circuit breaker is open"  # AC-2.3

def test_state_remains_open_after_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)  # advance to timeout
    # State should remain open after the timeout has elapsed
    assert breaker.state() == "open"  # AC-3.1

def test_successful_probe_closes_circuit():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)  # advance to timeout
    result = breaker.call(lambda: "recovered")
    # A successful probe should close the circuit
    assert result == "recovered"  # AC-3.2
    assert breaker.state() == "closed"  # AC-3.5

def test_failed_probe_reopens_circuit():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)  # advance to timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)
    # A failed probe should propagate the error
    assert str(excinfo.value) == "division by zero"  # AC-3.3
    assert breaker.state() == "open"  # AC-3.5

def test_failed_probe_resets_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)  # advance to timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)
    assert str(excinfo.value) == "division by zero"  # AC-3.3
    
    clock.advance(29.9)  # advance just before the second timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    assert str(excinfo.value) == "circuit breaker is open"  # AC-3.5

    clock.advance(0.1)  # advance to permit the next probe
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)
    # Expect the probe to run and raise the error instead of being blocked
    assert str(excinfo.value) == "division by zero"  # AC-3.6

def test_custom_failure_threshold():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock, failure_threshold=1)
    try:
        breaker.call(lambda: 1 / 0)
    except Exception:
        pass
    # A custom failure threshold of 1 should open immediately after one failure
    assert breaker.state() == "open"  # AC-4.1

def test_custom_reset_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock, reset_timeout=10)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(10)  # advance to custom reset timeout
    result = breaker.call(lambda: "recovered")
    # A successful probe after custom timeout should close the circuit
    assert result == "recovered"  # AC-4.2
    assert breaker.state() == "closed"  # AC-4.2

def test_rejection_just_before_custom_reset_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock, reset_timeout=10)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(9.9)  # advance just before custom timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    # Call should still be rejected just before custom timeout
    assert str(excinfo.value) == "circuit breaker is open"  # AC-4.2