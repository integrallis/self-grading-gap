# file: rate_limiter.py
from candidate import SlidingWindowThrottler


class RateLimiter:
    def __init__(self, max_requests, time_window, client_id):
        self._throttler = SlidingWindowThrottler(max_requests, time_window)
        self._client_id = client_id

    def allow_request(self, timestamp):
        return self._throttler.request(self._client_id, timestamp)
