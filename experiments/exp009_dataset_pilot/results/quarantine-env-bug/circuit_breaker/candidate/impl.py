import time

class CircuitBreakerError(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=30):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = 'CLOSED'
        self.failure_count = 0
        self.last_failure_time = None
        self.last_open_time = None

    def _reset(self):
        self.failure_count = 0
        self.last_open_time = None

    def _is_reset_timeout(self):
        if self.last_open_time is None:
            return False
        return (time.time() - self.last_open_time) >= self.reset_timeout

    def call(self, operation):
        if self.state == 'OPEN':
            if self._is_reset_timeout():
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerError("circuit breaker is open")

        try:
            result = operation()
            if self.state == 'CLOSED':
                self._reset()
            elif self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self._reset()
            return result
        except Exception as e:
            if self.state == 'CLOSED':
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.state = 'OPEN'
                    self.last_open_time = time.time()
            elif self.state == 'HALF_OPEN':
                self.state = 'OPEN'
                self.last_open_time = time.time()
            raise e
