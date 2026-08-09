import pytest
from solution import CircuitBreaker

class CircuitOpenError(Exception):
    pass

@pytest.fixture
def clock():
    class Clock:
        def __init__(self):
            self.current_time = 0
        
        def advance(self, seconds):
            self.current_time += seconds
        
        def now(self):
            return self.current_time
    
    return Clock()

def test_new_breaker_reports_closed_state():
    breaker = CircuitBreaker(clock=clock())
    # AC-1.1: New breaker reports the closed state.
    assert breaker.call(lambda: "success") == "success"  # Implicitly checks closed state

def test_successful_call_while_closed():
    breaker = CircuitBreaker(clock=clock())
    result = breaker.call(lambda: "success")  # AC-1.2: While closed, a successful call's result is returned unchanged.
    assert result == "success"

def test_failing_call_while_closed():
    breaker = CircuitBreaker(clock=clock())
    with pytest.raises(ZeroDivisionError) as exc:  # AC-1.3: A failing call's error propagates to the caller.
        breaker.call(lambda: 1 / 0)
    assert str(exc.value) == "division by zero"  # Ensure original error is propagated.

def test_consecutive_failures_below_threshold():
    breaker = CircuitBreaker(clock=clock())
    for _ in range(2):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    assert breaker.call(lambda: "success") == "success"  # Implicitly checks still closed.

def test_success_between_failures_resets_count():
    breaker = CircuitBreaker(clock=clock())
    for _ in range(2):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    breaker.call(lambda: "success")  # success resets failure count
    for _ in range(2):
        try:
            breaker.call(lambda: 1 / 0)  # induce further failures
        except Exception:
            pass
    assert breaker.call(lambda: "success") == "success"  # Implicitly checks still closed.

def test_reaching_failure_threshold_opens_circuit():
    breaker = CircuitBreaker(clock=clock())
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    with pytest.raises(CircuitOpenError) as exc:  # AC-2.2: Calls rejected with circuit-open error.
        breaker.call(lambda: "success")  # Should not invoke the lambda
    assert str(exc.value) == "circuit breaker is open"

def test_calls_rejected_while_open():
    breaker = CircuitBreaker(clock=clock())
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    with pytest.raises(CircuitOpenError) as exc:  # AC-2.2: Calls rejected with circuit-open error.
        breaker.call(lambda: "success")  # Should not invoke the lambda
    assert str(exc.value) == "circuit breaker is open"

def test_calls_rejected_during_reset_timeout(clock):
    breaker = CircuitBreaker(clock=clock())
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    clock.advance(29.9)  # Just before timeout
    with pytest.raises(CircuitOpenError) as exc:
        breaker.call(lambda: "success")  # AC-2.3: Calls rejected during the reset timeout.
    assert str(exc.value) == "circuit breaker is open"

def test_timeout_does_not_change_state(clock):
    breaker = CircuitBreaker(clock=clock())
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    clock.advance(30)  # wait for the reset timeout
    with pytest.raises(CircuitOpenError) as exc:  # Should remain open
        breaker.call(lambda: "success")  # Should not invoke the lambda
    assert str(exc.value) == "circuit breaker is open"  # AC-3.1: State remains open.

def test_successful_probe_closes_circuit(clock):
    breaker = CircuitBreaker(clock=clock())
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    clock.advance(30)  # wait for the reset timeout
    result = breaker.call(lambda: "success")  # AC-3.2: Probe call succeeds.
    assert result == "success"  # Ensure the successful result
    # Implicitly checks state is closed after success.

def test_failed_probe_reopens_circuit(clock):
    breaker = CircuitBreaker(clock=clock())
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    clock.advance(30)  # wait for the reset timeout
    with pytest.raises(ZeroDivisionError) as exc:
        breaker.call(lambda: 1 / 0)  # AC-3.3: Probe call fails.
    assert str(exc.value) == "division by zero"  # Ensure original error is propagated
    # Implicitly checks state reopens.

def test_failed_probe_resets_timeout(clock):
    breaker = CircuitBreaker(clock=clock())
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    clock.advance(30)  # wait for the reset timeout
    try:
        breaker.call(lambda: 1 / 0)  # Probe fails
    except Exception:
        pass
    clock.advance(30)  # wait for reset timeout again
    with pytest.raises(CircuitOpenError) as exc:
        breaker.call(lambda: "success")  # Should not be allowed yet
    assert str(exc.value) == "circuit breaker is open"
    clock.advance(30)  # Now should be allowed
    result = breaker.call(lambda: "success")
    assert result == "success"  # AC-3.4: Failed probe resets timeout.

def test_successful_recovery_starts_count_from_zero(clock):
    breaker = CircuitBreaker(clock=clock())
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    clock.advance(30)  # wait for the reset timeout
    breaker.call(lambda: "success")  # Probe succeeds
    # Implicitly checks state is closed after success.
    
    for _ in range(2):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    with pytest.raises(CircuitOpenError) as exc:
        breaker.call(lambda: "success")  # Should not invoke the lambda
    assert str(exc.value) == "circuit breaker is open"  # Ensure the circuit is still open.

def test_probe_permitted_exactly_after_timeout(clock):
    breaker = CircuitBreaker(clock=clock())
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    clock.advance(30)  # wait for the reset timeout
    result = breaker.call(lambda: "success")  # AC-3.6: Probe is allowed only when timeout has elapsed.
    assert result == "success"

def test_custom_failure_threshold():
    breaker = CircuitBreaker(clock=clock(), failure_threshold=1)
    with pytest.raises(ZeroDivisionError):
        breaker.call(lambda: 1 / 0)  # induce failure
    with pytest.raises(CircuitOpenError) as exc:  # AC-4.1: Circuit opens after single failure.
        breaker.call(lambda: "success")  # Should not invoke the lambda
    assert str(exc.value) == "circuit breaker is open"

def test_custom_reset_timeout(clock):
    breaker = CircuitBreaker(clock=clock(), reset_timeout=10)
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    clock.advance(10)  # wait for the custom reset timeout
    result = breaker.call(lambda: "success")  # Should be allowed now
    assert result == "success"  # AC-4.2: Custom reset timeout allows probe call.

def test_failed_operation_error_is_distinguished():
    breaker = CircuitBreaker(clock=clock())
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)  # induce failures
        except Exception:
            pass
    with pytest.raises(ZeroDivisionError) as exc:
        breaker.call(lambda: 1 / 0)  # Should raise on failure.
    assert str(exc.value) == "division by zero"  # Ensure original error is propagated.