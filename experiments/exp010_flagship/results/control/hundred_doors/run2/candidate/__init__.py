import pytest

def compute_door_states(door_count):
    if door_count < 0:
        raise ValueError("door count must be non-negative")
    if door_count == 0:
        return ([], [], "")

    # Initialize doors
    doors = [False] * door_count

    # Simulate the toggling of doors
    for walk in range(1, door_count + 1):
        for door in range(walk - 1, door_count, walk):
            doors[door] = not doors[door]

    # Collect open doors and indicators
    open_doors = [i + 1 for i in range(door_count) if doors[i]]
    indicators = ["@" if state else "#" for state in doors]
    state_string = "".join(indicators)
    return (indicators, open_doors, state_string)