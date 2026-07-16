import time

class CircuitBreaker:
    class CircuitOpenError(Exception):
        pass

    def __init__(self, failure_threshold=3, reset_timeout=30):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = 'CLOSED'
        self.failure_count = 0
        self.last_failure_time = None
        self.last_open_time = None

    def call(self, operation):
        current_time = time.monotonic()

        if self.state == 'CLOSED':
            try:
                result = operation()
                self._reset_failure_count()
                return result
            except Exception as e:
                self._record_failure(current_time)
                raise e

        elif self.state == 'OPEN':
            if self.last_open_time is None:
                raise self.CircuitOpenError("circuit breaker is open")

            if current_time - self.last_open_time >= self.reset_timeout:
                self.state = 'HALF_OPEN'
                return self._probe(operation)
            else:
                raise self.CircuitOpenError("circuit breaker is open")

        elif self.state == 'HALF_OPEN':
            return self._probe(operation)

    def _probe(self, operation):
        try:
            result = operation()
            self.state = 'CLOSED'
            self._reset_failure_count()
            return result
        except Exception as e:
            self._record_failure(time.monotonic())
            raise e

    def _record_failure(self, current_time):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
            self.last_open_time = current_time

    def _reset_failure_count(self):
        self.failure_count = 0
        self.last_open_time = None

    def reset(self):
        self.state = 'CLOSED'
        self._reset_failure_count()

    def is_open(self):
        return self.state == 'OPEN'
