import time
import pytest
from solution import CircuitBreaker

def test_new_breaker_reports_closed_state():
    breaker = CircuitBreaker()
    assert breaker.state == "closed"  # AC-1.1

def test_successful_call_while_closed():
    breaker = CircuitBreaker()
    result = breaker.call(lambda: "success")
    assert result == "success"  # AC-1.2

def test_failing_call_while_closed():
    breaker = CircuitBreaker()
    with pytest.raises(Exception):
        breaker.call(lambda: 1 / 0)  # AC-1.3

def test_consecutive_failures_below_threshold():
    breaker = CircuitBreaker()
    for _ in range(2):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    assert breaker.state == "closed"  # AC-1.4

def test_success_between_failures_resets_count():
    breaker = CircuitBreaker()
    try:
        breaker.call(lambda: 1 / 0)
    except Exception:
        pass
    result = breaker.call(lambda: "success")  # Reset count
    assert result == "success"  # AC-1.5
    assert breaker.state == "closed"  # Should still be closed

def test_reaches_failure_threshold_opens_circuit():
    breaker = CircuitBreaker()
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    assert breaker.state == "open"  # AC-2.1

def test_calls_rejected_while_open():
    breaker = CircuitBreaker()
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    with pytest.raises(Exception) as exc:
        breaker.call(lambda: "success")
    assert str(exc.value) == "circuit breaker is open"  # AC-2.2

def test_calls_rejected_during_reset_timeout():
    breaker = CircuitBreaker(reset_timeout=1)  # 1 second for test
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    time.sleep(0.5)
    with pytest.raises(Exception):
        breaker.call(lambda: "success")  # Still open during timeout

def test_timeout_does_not_change_reported_state():
    breaker = CircuitBreaker(reset_timeout=1)  # 1 second for test
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    time.sleep(1)  # Wait for the timeout
    assert breaker.state == "open"  # AC-3.1

def test_successful_probe_call_closes_circuit():
    breaker = CircuitBreaker(reset_timeout=1)  # 1 second for test
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    time.sleep(1)  # Wait for the timeout
    result = breaker.call(lambda: "success")  # Probe
    assert result == "success"  # AC-3.2
    assert breaker.state == "closed"  # Should close after success

def test_failed_probe_call_reopens_circuit():
    breaker = CircuitBreaker(reset_timeout=1)  # 1 second for test
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    time.sleep(1)  # Wait for the timeout
    try:
        breaker.call(lambda: 1 / 0)  # Probe
    except Exception:
        pass
    assert breaker.state == "open"  # AC-3.3

def test_failed_probe_resets_timeout():
    breaker = CircuitBreaker(reset_timeout=1)  # 1 second for test
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    time.sleep(1)  # Wait for the timeout
    try:
        breaker.call(lambda: 1 / 0)  # Failed probe
    except Exception:
        pass
    time.sleep(1)  # Wait for another timeout
    assert breaker.state == "open"  # AC-3.4

def test_successful_recovery_resets_failure_count():
    breaker = CircuitBreaker(reset_timeout=1)  # 1 second for test
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    time.sleep(1)  # Wait for the timeout
    result = breaker.call(lambda: "success")  # Probe
    assert result == "success"  # AC-3.5
    assert breaker.state == "closed"  # Circuit should close

    # Check that we need 3 more failures to reopen
    for _ in range(2):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    assert breaker.state == "closed"  # Still closed after 2 failures

def test_custom_failure_threshold():
    breaker = CircuitBreaker(failure_threshold=1)  # 1 failure to open
    try:
        breaker.call(lambda: 1 / 0)
    except Exception:
        pass
    assert breaker.state == "open"  # AC-4.1

def test_custom_reset_timeout():
    breaker = CircuitBreaker(reset_timeout=2)  # 2 seconds for test
    for _ in range(3):
        try:
            breaker.call(lambda: 1 / 0)
        except Exception:
            pass
    time.sleep(2)  # Wait for the timeout
    result = breaker.call(lambda: "success")  # Probe
    assert result == "success"  # AC-4.2
    assert breaker.state == "closed"  # Should close after success