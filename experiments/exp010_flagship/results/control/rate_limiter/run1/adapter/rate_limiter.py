# file: rate_limiter.py
from candidate import request_throttle as _request_throttle


class RateLimiter:
    def __init__(self, client_id, max_requests, time_window):
        self.client_id = client_id
        self.max_requests = max_requests
        self.time_window = time_window

    def allow_request(self, current_time):
        return _request_throttle(
            self.client_id,
            self.max_requests,
            self.time_window,
            current_time,
        )

    def raises(self, client_id, current_time):
        return _request_throttle(
            client_id,
            self.max_requests,
            self.time_window,
            current_time,
        )
