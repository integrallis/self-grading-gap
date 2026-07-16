# file: hundred_doors.py
from candidate import compute_door_states


def final_door_states(num_doors):
    return compute_door_states(num_doors)


def open_doors(num_doors):
    return compute_door_states(num_doors).open_positions


def render_doors(num_doors):
    return compute_door_states(num_doors).state_string
