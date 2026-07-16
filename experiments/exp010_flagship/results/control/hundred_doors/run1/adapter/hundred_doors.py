# file: hundred_doors.py
from candidate import compute_door_states


def final_door_states(n):
    states, _, _ = compute_door_states(n)
    return states


def open_doors(n):
    _, doors, _ = compute_door_states(n)
    return doors


def render_doors(n):
    _, _, rendered = compute_door_states(n)
    return rendered
