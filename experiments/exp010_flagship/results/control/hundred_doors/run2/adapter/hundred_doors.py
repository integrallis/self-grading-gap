# file: hundred_doors.py
from candidate import compute_door_states


def final_door_states(door_count):
    states, doors, rendered = compute_door_states(door_count)
    return states


def open_doors(door_count):
    states, doors, rendered = compute_door_states(door_count)
    return doors


def render_doors(door_count):
    states, doors, rendered = compute_door_states(door_count)
    return rendered
