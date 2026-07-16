# file: circuit_breaker.py
from candidate.impl import CircuitBreaker as _CircuitBreaker
from candidate.impl import CircuitBreakerError as CircuitOpenError


class CircuitState:
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker(_CircuitBreaker):
    execute = _CircuitBreaker.call
    raises = _CircuitBreaker.call
