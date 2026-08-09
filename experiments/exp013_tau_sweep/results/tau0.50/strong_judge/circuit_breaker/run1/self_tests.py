import pytest
from solution import CircuitBreaker

class FakeClock:
    def __init__(self):
        self.current_time = 0.0

    def advance(self, seconds):
        self.current_time += seconds

    def now(self):
        return self.current_time

def test_circuit_breaker_initial_state():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    assert cb.state == "closed"  # AC-1.1: A new breaker reports the closed state.

def test_circuit_breaker_pass_through_success():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    result = cb.call(lambda: "success")  # AC-1.2: Successful call's result is returned unchanged.
    assert result == "success"

def test_circuit_breaker_pass_through_failure():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    with pytest.raises(ZeroDivisionError) as excinfo:  # AC-1.3: Failing call's error propagates to the caller.
        cb.call(lambda: 1 / 0)
    assert excinfo.value.__class__ == ZeroDivisionError  # Check the original error type is propagated.
    assert cb.state == "closed"  # AC-1.5: Breaker stays closed after a failure.

def test_circuit_breaker_consecutive_failures_below_threshold():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    for _ in range(2):
        try:
            cb.call(lambda: 1 / 0)  # simulate failure
        except Exception:
            pass
    assert cb.state == "closed"  # AC-1.4: Breaker stays closed with 2 consecutive failures.

def test_circuit_breaker_success_resets_failure_count():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    for _ in range(2):
        try:
            cb.call(lambda: 1 / 0)  # simulate failure
        except Exception:
            pass
    cb.call(lambda: "success")  # reset failure count
    for _ in range(2):
        try:
            cb.call(lambda: 1 / 0)  # simulate further failures
        except Exception:
            pass
    assert cb.state == "closed"  # AC-1.5: Success resets consecutive-failure count.

def test_circuit_breaker_opens_on_threshold_exceeded():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0)  # simulate 3 failures
        except Exception:
            pass
    assert cb.state == "open"  # AC-2.1: Breaker opens after 3 consecutive failures.

def test_circuit_breaker_rejects_calls_when_open():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0)  # simulate 3 failures
        except Exception:
            pass
    with pytest.raises(Exception) as excinfo:  # AC-2.2: Calls are rejected with circuit-open error.
        cb.call(lambda: "success")
    assert str(excinfo.value) == "circuit breaker is open"  # Check error message.

def test_circuit_breaker_rejects_calls_just_before_timeout():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0)  # simulate 3 failures
        except Exception:
            pass
    clock.advance(29.999)  # advance time to just before timeout
    with pytest.raises(Exception) as excinfo:
        cb.call(lambda: "success")
    assert str(excinfo.value) == "circuit breaker is open"  # AC-2.3: Calls rejected just before timeout.

def test_circuit_breaker_probes_after_timeout():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)  # simulate waiting for reset timeout
    result = cb.call(lambda: "success")  # AC-3.2: Probe call after timeout should succeed.
    assert result == "success"
    assert cb.state == "closed"  # Circuit should close after successful probe.

def test_circuit_breaker_probe_fails():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)  # simulate waiting for reset timeout
    with pytest.raises(ZeroDivisionError):  # Probe fails
        cb.call(lambda: 1 / 0)  # AC-3.3: Check the probe's error propagates.
    assert cb.state == "open"  # AC-3.3: Circuit opens again after failing probe.

def test_circuit_breaker_probe_resets_timeout_on_failure():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)  # simulate waiting for reset timeout
    with pytest.raises(ZeroDivisionError):
        cb.call(lambda: 1 / 0)  # First probe fails
    clock.advance(29.999)  # just before new timeout
    with pytest.raises(Exception) as excinfo:
        cb.call(lambda: "success")
    assert str(excinfo.value) == "circuit breaker is open"  # Still open before new timeout
    clock.advance(0.001)  # now we hit the timeout
    result = cb.call(lambda: "success")  # Should be allowed now
    assert result == "success"  # AC-3.6: Probe is permitted exactly at the timeout.

def test_circuit_breaker_successful_recovery_starts_new_count():
    clock = FakeClock()
    cb = CircuitBreaker(clock)
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0)
        except Exception:
            pass
    clock.advance(30)  # simulate waiting for reset timeout
    cb.call(lambda: "success")  # Probe succeeds
    for _ in range(2):
        try:
            cb.call(lambda: 1 / 0)  # simulate failures after recovery
        except Exception:
            pass
    assert cb.state == "closed"  # Still closed after two failures
    try:
        cb.call(lambda: 1 / 0)  # final failure
    except Exception:
        pass
    assert cb.state == "open"  # AC-3.5: Circuit opens again after new threshold failures.

def test_circuit_breaker_custom_failure_threshold():
    clock = FakeClock()
    cb = CircuitBreaker(clock, failure_threshold=1)
    try:
        cb.call(lambda: 1 / 0)  # one failure
    except Exception:
        pass
    assert cb.state == "open"  # AC-4.1: Circuit opens after a single failure.

def test_circuit_breaker_custom_reset_timeout():
    clock = FakeClock()
    cb = CircuitBreaker(clock, reset_timeout=10)
    for _ in range(3):
        try:
            cb.call(lambda: 1 / 0)  # simulate failures
        except Exception:
            pass
    clock.advance(9.999)  # wait for just before custom reset timeout
    with pytest.raises(Exception) as excinfo:
        cb.call(lambda: "success")  # Should still be open
    assert str(excinfo.value) == "circuit breaker is open"  # Check error message
    clock.advance(0.001)  # now we hit the timeout
    result = cb.call(lambda: "success")  # Probe should succeed
    assert result == "success"
    assert cb.state == "closed"  # Circuit should close after successful probe.