def compute_door_states(n):
    if n < 0:
        raise Exception("door count must be non-negative")
    states = [False] * n
    open_positions = []
    for i in range(1, int(n**0.5) + 1):
        pos = i * i
        if pos <= n:
            states[pos - 1] = True
            open_positions.append(pos)
    markers = ''.join('@' if state else '#' for state in states)
    return states, open_positions, markers
