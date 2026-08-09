import pytest
from solution import CircuitBreaker  # Assuming the main class is CircuitBreaker

class FakeClock:
    def __init__(self):
        self.current_time = 0

    def advance(self, seconds):
        self.current_time += seconds

    def now(self):
        return self.current_time

def test_new_breaker_reports_closed_state():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    assert breaker.state == "closed"  # AC-1.1

def test_successful_call_while_closed():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    result = breaker.call(lambda: "success")
    assert result == "success"  # AC-1.2

def test_failing_call_while_closed():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)  # Simulating a failure
    assert str(excinfo.value) == "division by zero"  # Original error propagated
    assert breaker.state == "closed"  # AC-1.3

def test_consecutive_failures_below_threshold():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    for _ in range(2):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    assert breaker.state == "closed"  # AC-1.4

def test_success_between_failures_resets_count():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    for _ in range(2):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    result = breaker.call(lambda: "success")  # Success resets the count
    assert result == "success"  # AC-1.5
    assert breaker.state == "closed"

def test_reaching_failure_threshold_opens_circuit():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    assert breaker.state == "open"  # AC-2.1

def test_calls_rejected_when_open():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "success")  # Should be rejected
    assert str(excinfo.value) == "circuit breaker is open"  # AC-2.2

def test_calls_rejected_for_reset_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    clock.advance(30)  # Advance time to reach reset timeout
    result = breaker.call(lambda: "success")  # Should be a probe and succeed
    assert result == "success"  # AC-3.2
    assert breaker.state == "closed"  # Circuit should close

def test_timeout_does_not_change_state():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    clock.advance(30)  # Advance time to reach reset timeout
    assert breaker.state == "open"  # AC-3.1

def test_successful_probe_closes_circuit():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    clock.advance(30)  # Advance time to reach reset timeout
    result = breaker.call(lambda: "success")  # Probe call
    assert result == "success"  # AC-3.2
    assert breaker.state == "closed"  # Circuit should close

def test_failed_probe_reopens_circuit():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    clock.advance(30)  # Advance time to reach reset timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: 1 / 0)  # Simulating a failure in probe
    assert str(excinfo.value) == "division by zero"  # Original error propagated
    assert breaker.state == "open"  # AC-3.3

def test_failed_probe_restarts_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    clock.advance(30)  # Advance time to reach reset timeout
    with pytest.raises(Exception):
        breaker.call(lambda: 1 / 0)  # Simulating a failure in probe
    assert breaker.state == "open"  # Still open after failed probe
    clock.advance(30)  # Advance time again
    result = breaker.call(lambda: "success")  # Should be permitted
    assert result == "success"  # New probe after timeout
    assert breaker.state == "closed"  # Circuit should close again

def test_successful_recovery_starts_count_over():
    clock = FakeClock()
    breaker = CircuitBreaker(clock)
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    clock.advance(30)  # Advance time to reach reset timeout
    result = breaker.call(lambda: "success")  # Probe call
    assert result == "success"  # AC-3.2
    for _ in range(2):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    assert breaker.state == "closed"  # Still closed after two failures
    with pytest.raises(Exception):
        breaker.call(lambda: 1 / 0)  # Third failure should open circuit
    assert breaker.state == "open"  # AC-3.5

def test_custom_failure_threshold():
    clock = FakeClock()
    breaker = CircuitBreaker(clock, failure_threshold=1)
    with pytest.raises(Exception):
        breaker.call(lambda: 1 / 0)  # Should open after 1 failure
    assert breaker.state == "open"  # AC-4.1

def test_custom_reset_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock, reset_timeout=10)
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    clock.advance(10)  # Advance time to reach custom reset timeout
    result = breaker.call(lambda: "success")  # Probe call
    assert result == "success"  # AC-4.2

def test_rejects_at_custom_timeout_boundary():
    clock = FakeClock()
    breaker = CircuitBreaker(clock, reset_timeout=10)
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(lambda: 1 / 0)  # Simulating a failure
    clock.advance(9)  # Advance time to just before custom reset timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "success")  # Should be rejected
    assert str(excinfo.value) == "circuit breaker is open"  # Circuit is still open
    clock.advance(1)  # Advance to the exact boundary
    result = breaker.call(lambda: "success")  # Should be permitted now
    assert result == "success"  # New probe after timeout
    assert breaker.state == "closed"  # Circuit should close again