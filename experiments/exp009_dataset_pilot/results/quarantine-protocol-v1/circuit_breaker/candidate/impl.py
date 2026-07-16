import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=30, clock=None):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.clock = clock or time.time
        self.state = "CLOSED"
        self.failure_count = 0
        self.last_failure_time = 0

    def call(self, operation):
        if self.state == "OPEN":
            if self.clock() - self.last_failure_time >= self.reset_timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("circuit breaker is open")

        try:
            result = operation()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            self.failure_count = 0
        else:
            self.failure_count = 0

    def _on_failure(self):
        if self.state == "CLOSED":
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_failure_time = self.clock()
        elif self.state == "HALF_OPEN":
            self.state = "OPEN"
            self.last_failure_time = self.clock()

    def get_state(self):
        return self.state
