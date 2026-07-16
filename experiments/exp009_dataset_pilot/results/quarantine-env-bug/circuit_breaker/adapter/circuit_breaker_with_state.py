# file: circuit_breaker_with_state.py

from candidate.impl import CircuitBreaker as _CircuitBreaker
from candidate.impl import CircuitBreakerError as _CircuitOpenError
from candidate.impl import CircuitBreaker as _CircuitState

class CircuitBreaker(_CircuitBreaker):
    pass

CircuitOpenError = _CircuitOpenError

class CircuitState:
    @staticmethod
    def get_state(circuit_breaker):
        return circuit_breaker.state
