# file: circuit_breaker.py
from candidate.impl import CircuitBreaker, CircuitOpenError

CircuitBreaker.execute = CircuitBreaker.call
