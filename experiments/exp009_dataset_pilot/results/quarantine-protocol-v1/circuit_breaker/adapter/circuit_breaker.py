# file: circuit_breaker.py
from candidate.impl import CircuitBreaker as ImplCircuitBreaker

class CircuitBreaker(ImplCircuitBreaker):
    pass

class CircuitOpenError(Exception):
    pass

class CircuitState:
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"
