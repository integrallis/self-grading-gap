import pytest

def compute_door_states(num_doors):
    if num_doors < 0:
        raise ValueError("door count must be non-negative")

    states = [False] * num_doors
    for walk in range(1, num_doors + 1):
        for door in range(walk - 1, num_doors, walk):
            states[door] = not states[door]

    open_positions = [i + 1 for i, state in enumerate(states) if state]
    state_string = ''.join('@' if state else '#' for state in states)

    return states, open_positions, state_string