# file: circuit_breaker.py
from candidate import CircuitBreaker as _CandidateCircuitBreaker


CircuitOpenError = Exception
CircuitState = str


class CircuitBreaker(_CandidateCircuitBreaker):
    def execute(self, *args):
        return self.call(*args)

    def raises(self, *args):
        return self.call(*args)
