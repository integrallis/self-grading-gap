# file: circuit_breaker.py

from candidate.impl import CircuitBreaker as ImplCircuitBreaker
from candidate.impl import CircuitBreaker as ImplCircuitBreaker, CircuitOpenError as ImplCircuitOpenError
from candidate.impl import CircuitBreaker as ImplCircuitBreaker, CircuitOpenError as ImplCircuitOpenError, CircuitState as ImplCircuitState

class CircuitState:
    CLOSED = 'CLOSED'
    OPEN = 'OPEN'
    HALF_OPEN = 'HALF_OPEN'

class CircuitBreaker:
    def __init__(self, *args):
        self._impl = ImplCircuitBreaker(*args)

    def execute(self, *args):
        return self._impl.call(*args)

    def reset(self):
        self._impl.reset()

    def is_open(self):
        return self._impl.is_open()

class CircuitOpenError(ImplCircuitOpenError):
    pass

# Expose CircuitState
CircuitState = CircuitState
