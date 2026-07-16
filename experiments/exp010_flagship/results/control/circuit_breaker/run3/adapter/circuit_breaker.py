# file: circuit_breaker.py
from candidate import CircuitBreaker as CircuitBreaker

CircuitBreaker.execute = CircuitBreaker.call
CircuitBreaker.raises = CircuitBreaker.call

CircuitOpenError = Exception
CircuitState = str
