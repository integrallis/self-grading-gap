import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=1):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.state = 'closed'
        self.last_failure_time = None

    def call(self, func):
        if self.state == 'open':
            if self.last_failure_time is None or time.time() - self.last_failure_time >= self.reset_timeout:
                self.state = 'half-open'
            else:
                raise Exception('circuit breaker is open')

        try:
            result = func()
            self.reset()  # Reset on success
            return result
        except Exception:
            if self.state == 'half-open':
                self.state = 'open'  # Transition to 'open' if the probe fails
            self.record_failure()  # Record failure
            raise

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = 'open'
            self.last_failure_time = time.time()

    def reset(self):
        self.failure_count = 0
        self.state = 'closed'