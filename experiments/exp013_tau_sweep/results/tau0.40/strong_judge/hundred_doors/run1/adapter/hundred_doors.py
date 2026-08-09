# file: hundred_doors.py
from candidate import compute_door_states as _compute_door_states


def final_door_states(n):
    states, positions, markers = _compute_door_states(n)
    return states


def open_doors(n):
    states, positions, markers = _compute_door_states(n)
    return positions


def render_doors(n):
    states, positions, markers = _compute_door_states(n)
    return markers
