# file: circuit_breaker.py

from candidate.impl import CircuitBreaker as _CircuitBreaker
from candidate.impl import CircuitBreakerError as _CircuitOpenError

class CircuitBreaker(_CircuitBreaker):
    pass

CircuitOpenError = _CircuitOpenError
