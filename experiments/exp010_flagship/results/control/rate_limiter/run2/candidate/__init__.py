class Throttle:
    def __init__(self, max_requests, time_window):
        if max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if time_window <= 0:
            raise ValueError("time_window must be positive")
        self.max_requests = max_requests
        self.time_window = time_window
        self.clients = {}

    def request(self, client_id, timestamp):
        if client_id not in self.clients:
            self.clients[client_id] = []

        # Remove timestamps that are out of the time window
        self.clients[client_id] = [t for t in self.clients[client_id] if t > timestamp - self.time_window]

        # Check if the client can make a new request
        if len(self.clients[client_id]) < self.max_requests:
            self.clients[client_id].append(timestamp)
            return True
        return False