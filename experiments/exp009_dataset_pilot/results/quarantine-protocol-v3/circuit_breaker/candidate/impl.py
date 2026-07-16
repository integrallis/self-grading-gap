# candidate/impl.py

import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=30, clock=time):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.clock = clock
        self.state = 'CLOSED'
        self.failure_count = 0
        self.last_failure_time = None
        self.open_time = None

    def call(self, operation):
        if self.state == 'OPEN':
            if self.clock.time() - self.open_time < self.reset_timeout:
                raise CircuitOpenError("circuit breaker is open")
            else:
                self.state = 'HALF_OPEN'

        try:
            result = operation()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        if self.state == 'CLOSED':
            self.failure_count = 0
        elif self.state == 'HALF_OPEN':
            self.state = 'CLOSED'
            self.failure_count = 0

    def _on_failure(self):
        if self.state == 'CLOSED':
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
                self.open_time = self.clock.time()
        elif self.state == 'HALF_OPEN':
            self.state = 'OPEN'
            self.open_time = self.clock.time()

class CircuitOpenError(Exception):
    pass
