# file: circuit_state.py

from candidate.impl import CircuitBreaker as _CircuitBreaker

class CircuitState:
    @staticmethod
    def get_state(circuit_breaker):
        return circuit_breaker.state
