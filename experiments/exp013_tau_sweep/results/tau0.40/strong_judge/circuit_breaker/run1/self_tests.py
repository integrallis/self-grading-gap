import time
import pytest
from solution import CircuitBreaker

class FakeClock:
    def __init__(self):
        self.current_time = 0

    def advance(self, seconds):
        self.current_time += seconds

    def now(self):
        return self.current_time

def test_new_breaker_reports_closed_state():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    # The initial state should be closed
    assert breaker.call(lambda: "success") == "success"  # AC-1.1

def test_successful_call_while_closed():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    result = breaker.call(lambda: "success")
    assert result == "success"  # AC-1.2

def test_failing_call_while_closed():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)
    assert str(excinfo.value) == "division by zero"  # AC-1.3

def test_consecutive_failures_below_threshold():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(2):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    assert breaker.call(lambda: "success") == "success"  # AC-1.4

def test_success_between_failures_resets_count():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    try:
        breaker.call(lambda: 1 / 0)
    except Exception:
        pass
    result = breaker.call(lambda: "success")
    assert result == "success"  # AC-1.5
    try:
        breaker.call(lambda: 1 / 0)
    except Exception:
        pass
    try:
        breaker.call(lambda: 1 / 0)
    except Exception:
        pass
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)
    assert str(excinfo.value) == "division by zero"  # AC-1.5

def test_open_circuit_after_failure_threshold():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    assert str(excinfo.value) == "circuit breaker is open"  # AC-2.1

def test_calls_rejected_when_open():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    assert str(excinfo.value) == "circuit breaker is open"  # AC-2.2

def test_rejects_calls_during_reset_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(29)
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    assert str(excinfo.value) == "circuit breaker is open"  # AC-2.3

def test_probe_call_after_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)
    result = breaker.call(lambda: "success")
    assert result == "success"  # AC-3.2

def test_failed_probe_reopens_circuit():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)
    assert str(excinfo.value) == "division by zero"  # AC-3.3

def test_failed_probe_resets_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)
    assert str(excinfo.value) == "division by zero"  # AC-3.3
    clock.advance(10)
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    assert str(excinfo.value) == "circuit breaker is open"  # AC-3.4

def test_successful_recovery_resets_failure_count():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)
    result = breaker.call(lambda: "success")
    assert result == "success"  # AC-3.2
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)
    assert str(excinfo.value) == "circuit breaker is open"  # AC-3.5

def test_custom_failure_threshold():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock, failure_threshold=1)
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)
    assert str(excinfo.value) == "division by zero"  # Expecting the original exception
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    assert str(excinfo.value) == "circuit breaker is open"  # AC-4.1

def test_custom_reset_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock, reset_timeout=10)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(9)
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not be called")
    assert str(excinfo.value) == "circuit breaker is open"  # AC-4.2
    clock.advance(1)
    result = breaker.call(lambda: "success")
    assert result == "success"  # AC-4.2