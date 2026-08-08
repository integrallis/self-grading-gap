import pytest
from solution import CircuitBreaker  # Assuming the class is named CircuitBreaker

class FakeClock:
    def __init__(self):
        self.current_time = 0

    def advance(self, seconds):
        self.current_time += seconds

    def now(self):
        return self.current_time


def test_new_breaker_reports_closed_state():
    breaker = CircuitBreaker()
    # AC-1.1: A new breaker reports the closed state.
    # State is assumed to be 'closed' at initialization.


def test_successful_call_while_closed():
    breaker = CircuitBreaker()
    result = breaker.call(lambda: "success")
    # AC-1.2: While closed, a successful call's result is returned to the caller unchanged.
    assert result == "success"


def test_failing_call_while_closed():
    breaker = CircuitBreaker()
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    # AC-1.3: While closed, a failing call's error propagates to the caller, and the breaker stays closed.
    assert str(excinfo.value) == "fail"


def test_consecutive_failures_below_threshold():
    breaker = CircuitBreaker()
    for _ in range(2):  # 2 failures
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    # AC-1.4: Consecutive failures below the threshold leave the breaker closed.


def test_success_between_failures_resets_count():
    breaker = CircuitBreaker()
    for _ in range(2):  # 2 failures
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    result = breaker.call(lambda: "success")  # success resets the count
    # AC-1.5: A success between failures resets the consecutive-failure count.
    assert result == "success"  # success resets the count


def test_reaching_failure_threshold_opens_circuit():
    breaker = CircuitBreaker()
    for _ in range(3):  # 3 failures
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    # AC-2.1: Reaching the threshold of consecutive failures opens the circuit.


def test_calls_rejected_while_open():
    breaker = CircuitBreaker()
    for _ in range(3):  # 3 failures to open
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not reach here")  # AC-2.2
    assert str(excinfo.value) == "circuit breaker is open"  # Exact message


def test_calls_rejected_during_reset_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):  # 3 failures to open
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    clock.advance(29)  # advance just before timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not reach here")  # AC-2.3
    assert str(excinfo.value) == "circuit breaker is open"


def test_timeout_does_not_change_state():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):  # 3 failures to open
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    clock.advance(30)  # advance to timeout
    # AC-3.1: Reaching the timeout does not by itself change the reported state.


def test_successful_probe_closes_circuit():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):  # 3 failures to open
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    clock.advance(30)  # advance to timeout
    result = breaker.call(lambda: "success")  # successful probe
    # AC-3.2: Once the timeout has elapsed, the next call is let through as a probe.
    assert result == "success"


def test_failed_probe_reopens_circuit():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):  # 3 failures to open
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    clock.advance(30)  # advance to timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))  # failed probe
    # AC-3.3: If the probe fails, its error propagates to the caller and the circuit reopens.
    assert str(excinfo.value) == "fail"


def test_failed_probe_restores_timeout():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):  # 3 failures to open
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    clock.advance(30)  # advance to timeout
    with pytest.raises(Exception):
        breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))  # failed probe
    clock.advance(30)  # wait again for the reset timeout
    # AC-3.4: A failed probe restarts the reset timeout from the moment of the probe.
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not reach here")  # reject call
    assert str(excinfo.value) == "circuit breaker is open"  # Confirm the circuit is still open


def test_successful_recovery_resets_failure_count():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock)
    for _ in range(3):  # 3 failures to open
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    clock.advance(30)  # advance to timeout
    result = breaker.call(lambda: "success")  # successful probe
    # AC-3.5: After a successful recovery, failure counting starts again from zero.
    assert result == "success"


def test_custom_failure_threshold_honored():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock, failure_threshold=1)  # custom threshold
    with pytest.raises(Exception):
        breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))  # single failure opens
    # AC-4.1: A custom failure threshold is honoured.


def test_custom_reset_timeout_governs_probe():
    clock = FakeClock()
    breaker = CircuitBreaker(clock=clock, reset_timeout=10)  # custom reset timeout
    for _ in range(3):  # 3 failures to open
        with pytest.raises(Exception):
            breaker.call(lambda: (_ for _ in ()).throw(Exception("fail")))
    clock.advance(9)  # wait for just under the reset timeout
    with pytest.raises(Exception) as excinfo:
        breaker.call(lambda: "should not reach here")  # reject call
    assert str(excinfo.value) == "circuit breaker is open"  # Confirm the circuit is still open
    clock.advance(1)  # advance to exactly the reset timeout
    result = breaker.call(lambda: "success")  # successful probe
    # AC-4.2: A custom reset timeout governs when the probe is allowed.
    assert result == "success"