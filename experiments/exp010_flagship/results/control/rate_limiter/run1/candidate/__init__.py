def request_throttle(client_id, max_requests, time_window, current_time):
    if max_requests <= 0:
        raise ValueError("max_requests must be positive")
    if time_window <= 0:
        raise ValueError("time_window must be positive")

    if client_id not in request_logs:
        request_logs[client_id] = []

    # Clean up old requests outside the time window
    while request_logs[client_id] and request_logs[client_id][0] <= current_time - time_window:
        request_logs[client_id].pop(0)

    # Check if we can approve the new request
    if len(request_logs[client_id]) < max_requests:
        request_logs[client_id].append(current_time)
        return True
    else:
        return False

request_logs = {}