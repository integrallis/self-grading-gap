class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=5):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = 'closed'
        self.failure_count = 0
        self.last_failure_time = None

    def call(self, func):
        if self.state == 'open':
            if time.time() - self.last_failure_time >= self.reset_timeout:
                self.state = 'closed'
            else:
                raise Exception('circuit breaker is open')

        try:
            result = func()
            self.failure_count = 0  # Reset on success
            return result
        except Exception:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = 'open'
            raise