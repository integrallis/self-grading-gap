# file: rate_limiter.py
from candidate import Throttle


class RateLimiter(Throttle):
    def __init__(self, max_requests, time_window, timestamp):
        super().__init__(max_requests, time_window)
        self.timestamp = timestamp

    def allow_request(self, client_id):
        return self.request(client_id, self.timestamp)

    raises = Throttle.request
