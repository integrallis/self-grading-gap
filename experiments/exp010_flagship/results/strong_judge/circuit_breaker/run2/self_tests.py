import pytest
from solution import *  # Import everything from the solution package

def test_initial_state_is_closed():
    cb = CircuitBreaker(clock=lambda: 0)  # Using a simple clock that returns 0
    assert cb.reported_state() == "closed"  # AC-1.1: A new breaker reports the closed state.

def test_successful_call_passes_through_while_closed():
    cb = CircuitBreaker(clock=lambda: 0)
    result = cb.call(lambda: "Success")
    assert result == "Success"  # AC-1.2: While closed, a successful call's result is returned to the caller unchanged.

def test_failing_call_propagates_error_while_closed():
    cb = CircuitBreaker(clock=lambda: 0)
    with pytest.raises(Exception, match="Failure"):
        cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))  # AC-1.3: While closed, a failing call's error propagates to the caller.

def test_consecutive_failures_below_threshold_leaves_closed():
    cb = CircuitBreaker(clock=lambda: 0)
    for _ in range(2):  # Two failures
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))
        except Exception:
            pass
    assert cb.reported_state() == "closed"  # AC-1.4: Consecutive failures below the threshold leave the breaker closed.

def test_success_between_failures_resets_count():
    cb = CircuitBreaker(clock=lambda: 0)
    with pytest.raises(Exception, match="Failure"):
        cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))  # First failure
    cb.call(lambda: "Success")  # Success should reset the count
    with pytest.raises(Exception, match="Failure"):
        cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))  # Second failure
    assert cb.reported_state() == "closed"  # AC-1.5: A success between failures resets the consecutive-failure count.

def test_opens_circuit_after_threshold_reached():
    cb = CircuitBreaker(clock=lambda: 0)
    for _ in range(3):  # Three consecutive failures
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))
        except Exception:
            pass
    assert cb.reported_state() == "open"  # AC-2.1: Reaching the threshold of consecutive failures opens the circuit.

def test_calls_rejected_when_circuit_is_open():
    cb = CircuitBreaker(clock=lambda: 0)
    for _ in range(3):
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))
        except Exception:
            pass
    with pytest.raises(Exception) as exc_info:
        cb.call(lambda: "Should not execute")  # AC-2.2: Calls are rejected with a dedicated error.
    assert str(exc_info.value) == "circuit breaker is open"  # Exact error message check

def test_state_stays_open_until_probe_attempted():
    cb = CircuitBreaker(clock=lambda: 0)
    for _ in range(3):
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))
        except Exception:
            pass
    assert cb.reported_state() == "open"  # AC-3.1: Reaching the timeout does not change the reported state.

def test_successful_probe_closes_circuit():
    cb = CircuitBreaker(clock=lambda: 0)
    for _ in range(3):
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))
        except Exception:
            pass
    cb.advance_time(30)  # Simulate waiting for reset timeout
    result = cb.call(lambda: "Success")  # This should be a probe
    assert result == "Success"  # AC-3.2: A successful probe returns its result and closes the circuit.
    assert cb.reported_state() == "closed"  # Circuit is closed again.

def test_failed_probe_reopens_circuit():
    cb = CircuitBreaker(clock=lambda: 0)
    for _ in range(3):
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))
        except Exception:
            pass
    cb.advance_time(30)  # Simulate waiting for reset timeout
    with pytest.raises(Exception, match="Probe Failure"):
        cb.call(lambda: (_ for _ in ()).throw(Exception("Probe Failure")))  # This should be a probe
    assert cb.reported_state() == "open"  # AC-3.3: A failed probe propagates error.

def test_failed_probe_resets_timeout():
    cb = CircuitBreaker(clock=lambda: 0)
    for _ in range(3):
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))
        except Exception:
            pass
    cb.advance_time(30)  # Simulate waiting for reset timeout
    with pytest.raises(Exception, match="Probe Failure"):
        cb.call(lambda: (_ for _ in ()).throw(Exception("Probe Failure")))  # This should be a probe

    cb.advance_time(30)  # Simulate waiting another 30 seconds
    result = cb.call(lambda: "Success")  # This should be a probe
    assert result == "Success"  # Probe should succeed now
    assert cb.reported_state() == "closed"  # Circuit should be closed after successful probe.

def test_custom_failure_threshold():
    cb = CircuitBreaker(failure_threshold=1, clock=lambda: 0)  # Setting threshold to 1
    with pytest.raises(Exception, match="Failure"):
        cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))  # This should open the circuit
    assert cb.reported_state() == "open"  # AC-4.1: A custom failure threshold is honoured.

def test_custom_reset_timeout():
    cb = CircuitBreaker(reset_timeout=10, clock=lambda: 0)  # Setting reset timeout to 10 seconds
    for _ in range(3):
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))
        except Exception:
            pass
    cb.advance_time(10)  # Simulate waiting for the custom reset timeout
    result = cb.call(lambda: "Success")  # This should be a probe
    assert result == "Success"  # AC-4.2: Custom reset timeout governs probe timing.
    assert cb.reported_state() == "closed"  # Circuit should be closed after successful probe.

def test_not_a_moment_before_timeout():
    cb = CircuitBreaker(clock=lambda: 0)
    for _ in range(3):
        try:
            cb.call(lambda: (_ for _ in ()).throw(Exception("Failure")))
        except Exception:
            pass
    cb.advance_time(29.9)  # Just before the timeout
    with pytest.raises(Exception, match="circuit breaker is open"):
        cb.call(lambda: "Should not execute")  # Should still be open

    cb.advance_time(0.1)  # Exactly at the timeout
    result = cb.call(lambda: "Success")  # This should be a probe
    assert result == "Success"  # Should succeed now
    assert cb.reported_state() == "closed"  # Circuit should be closed after successful probe.