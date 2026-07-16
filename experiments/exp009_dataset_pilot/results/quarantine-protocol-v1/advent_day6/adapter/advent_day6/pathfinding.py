# file: advent_day6/pathfinding.py

from candidate.impl import GuardPatrolMap

def calculate_grid(map_text):
    """Adapt the grid calculation."""
    patrol = GuardPatrolMap(map_text)
    return patrol.grid

def calculate_next_location(map_text):
    """Calculate the next guard location."""
    patrol = GuardPatrolMap(map_text)
    return patrol.next_guard_location()

def calculate_path(map_text):
    """Calculate the path marked by the guard's walk."""
    patrol = GuardPatrolMap(map_text)
    return patrol.trace_guard_walk()

def find_start_position(map_text):
    """Find the starting position of the guard."""
    patrol = GuardPatrolMap(map_text)
    return patrol.find_guard_position()
