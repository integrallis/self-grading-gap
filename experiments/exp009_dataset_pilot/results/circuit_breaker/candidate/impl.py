import time

class CircuitBreakerError(Exception):
    """Custom exception to be raised when the circuit breaker is open."""
    def __init__(self):
        super().__init__("circuit breaker is open")


class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=30, clock=time.time):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.clock = clock
        self.state = 'CLOSED'
        self.failure_count = 0
        self.last_opened_time = 0

    def call(self, operation, *args, **kwargs):
        current_time = self.clock()

        if self.state == 'CLOSED':
            try:
                result = operation(*args, **kwargs)
                self.failure_count = 0  # Reset failure count on success
                return result
            except Exception as e:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.state = 'OPEN'
                    self.last_opened_time = current_time
                raise e

        elif self.state == 'OPEN':
            if current_time - self.last_opened_time >= self.reset_timeout:
                self.state = 'HALF_OPEN'
                return self._probe(operation, *args, **kwargs)
            else:
                raise CircuitBreakerError()

        elif self.state == 'HALF_OPEN':
            return self._probe(operation, *args, **kwargs)

    def _probe(self, operation, *args, **kwargs):
        try:
            result = operation(*args, **kwargs)
            self.state = 'CLOSED'  # Successful probe closes the circuit
            self.failure_count = 0  # Reset failure count
            return result
        except Exception as e:
            self.state = 'OPEN'  # Failed probe opens the circuit
            self.last_opened_time = self.clock()  # Restart reset timeout
            raise e
