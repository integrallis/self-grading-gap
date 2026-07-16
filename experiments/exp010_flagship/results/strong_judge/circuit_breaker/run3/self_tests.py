import pytest
from solution import CircuitBreaker

def test_initial_state_closed():
    cb = CircuitBreaker()
    # Assert that the initial state is closed; AC-1.1
    assert cb.state == 'closed'  # Implementation-dependent

def test_successful_call_while_closed():
    cb = CircuitBreaker()
    result = cb.call(lambda: "success")
    # Assert that a successful call returns the result unchanged; AC-1.2
    assert result == "success"

def test_failing_call_while_closed():
    cb = CircuitBreaker()
    with pytest.raises(ZeroDivisionError) as exc_info:
        cb.call(lambda: 1 / 0)  # Simulating failure
    # Assert that the original failure is propagated; AC-1.3
    assert isinstance(exc_info.value, ZeroDivisionError)

def test_consecutive_failures_below_threshold():
    cb = CircuitBreaker()
    for _ in range(2):
        try:
            cb.call(lambda: 1 / 0)  # Simulating failure
        except Exception:
            pass
    # Assert that the circuit remains closed after 2 failures; AC-1.4
    assert cb.state == 'closed'  # Implementation-dependent

def test_success_resets_failure_count():
    cb = CircuitBreaker()
    for _ in range(2):
        try:
            cb.call(lambda: 1 / 0)  # Simulating failure
        except Exception:
            pass
    cb.call(lambda: "success")  # Success resets the count
    try:
        cb.call(lambda: 1 / 0)  # Simulating failure again
    except Exception:
        pass
    # Assert that the circuit remains closed; AC-1.5
    assert cb.state == 'closed'  # Implementation-dependent

def test_open_circuit_after_threshold_reached():
    cb = CircuitBreaker()
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0)  # Simulating failure
        except Exception:
            pass
    # Assert that the circuit opens after 3 failures; AC-2.1
    assert cb.state == 'open'  # Implementation-dependent

def test_reject_calls_when_open():
    cb = CircuitBreaker()
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0)  # Simulating failure
        except Exception:
            pass
    with pytest.raises(Exception) as exc_info:
        cb.call(lambda: "success")
    # Assert that rejection uses the dedicated error message; AC-2.2
    assert str(exc_info.value) == "circuit breaker is open"

def test_reject_calls_just_before_reset_timeout():
    cb = CircuitBreaker()
    clock = FakeClock()
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0, clock=clock)  # Simulating failure
        except Exception:
            pass
    clock.advance(29)  # Advance time just before timeout
    with pytest.raises(Exception) as exc_info:
        cb.call(lambda: "success", clock=clock)  # Should reject
    assert str(exc_info.value) == "circuit breaker is open"  # AC-2.3

def test_probe_call_success_after_timeout():
    cb = CircuitBreaker()
    clock = FakeClock()
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0, clock=clock)  # Simulating failure
        except Exception:
            pass
    clock.advance(30)  # Advance to timeout
    result = cb.call(lambda: "success", clock=clock)  # Probe call
    # Assert that the result is returned and circuit closes; AC-3.2
    assert result == "success"
    # Assert state changes to closed; AC-3.5
    assert cb.state == 'closed'  # Implementation-dependent

def test_probe_call_failure_after_timeout():
    cb = CircuitBreaker()
    clock = FakeClock()
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0, clock=clock)  # Simulating failure
        except Exception:
            pass
    clock.advance(30)  # Advance to timeout
    with pytest.raises(ZeroDivisionError) as exc_info:
        cb.call(lambda: 1 / 0, clock=clock)  # Probe call fails
    # Assert that the original failure is propagated; AC-3.3
    assert isinstance(exc_info.value, ZeroDivisionError)

def test_failed_probe_resets_timeout():
    cb = CircuitBreaker()
    clock = FakeClock()
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0, clock=clock)  # Simulating failure
        except Exception:
            pass
    clock.advance(30)  # Advance to timeout
    with pytest.raises(ZeroDivisionError):
        cb.call(lambda: 1 / 0, clock=clock)  # Probe call fails
    clock.advance(29)  # Advance just before the new timeout
    with pytest.raises(Exception) as exc_info:
        cb.call(lambda: "success", clock=clock)  # Should reject
    assert str(exc_info.value) == "circuit breaker is open"  # AC-3.4

def test_successful_recovery_resets_failure_count():
    cb = CircuitBreaker()
    clock = FakeClock()
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0, clock=clock)  # Simulating failure
        except Exception:
            pass
    clock.advance(30)  # Advance to timeout
    cb.call(lambda: "success", clock=clock)  # Probe call
    for _ in range(2):
        try:
            cb.call(lambda: 1 / 0, clock=clock)  # Simulating failure
        except Exception:
            pass
    # Assert that the circuit remains closed after two new failures; AC-3.5
    assert cb.state == 'closed'  # Implementation-dependent
    try:
        cb.call(lambda: 1 / 0, clock=clock)  # Simulating failure
    except Exception:
        pass
    # Now it should be open after the third failure
    assert cb.state == 'open'  # Implementation-dependent

def test_custom_failure_threshold():
    cb = CircuitBreaker(failure_threshold=1)  # AC-4.1
    try:
        cb.call(lambda: 1 / 0)  # Simulating failure
    except Exception:
        pass
    # Assert that the circuit opens after 1 failure
    assert cb.state == 'open'  # Implementation-dependent

def test_custom_reset_timeout():
    cb = CircuitBreaker(reset_timeout=10)  # AC-4.2
    clock = FakeClock()
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0, clock=clock)  # Simulating failure
        except Exception:
            pass
    clock.advance(10)  # Advance to timeout
    result = cb.call(lambda: "success", clock=clock)  # Should be allowed
    assert result == "success"  # AC-4.2

def test_reject_calls_just_before_custom_reset_timeout():
    cb = CircuitBreaker(reset_timeout=10)  # AC-4.2
    clock = FakeClock()
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0, clock=clock)  # Simulating failure
        except Exception:
            pass
    clock.advance(9)  # Advance time just before timeout
    with pytest.raises(Exception) as exc_info:
        cb.call(lambda: "success", clock=clock)  # Should reject
    assert str(exc_info.value) == "circuit breaker is open"  # AC-4.2

class FakeClock:
    def __init__(self):
        self.current_time = 0

    def advance(self, seconds):
        self.current_time += seconds

    def now(self):
        return self.current_time