# file: circuit_breaker.py
from candidate import CircuitBreaker as _CircuitBreaker

CircuitOpenError = Exception
CircuitState = str


class CircuitBreaker(_CircuitBreaker):
    execute = _CircuitBreaker.call
