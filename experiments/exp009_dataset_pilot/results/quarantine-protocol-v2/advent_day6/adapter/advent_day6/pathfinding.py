# file: advent_day6/pathfinding.py

from candidate.impl import GuardPatrolMap

def calculate_grid(map_text):
    guard_patrol_map = GuardPatrolMap(map_text)
    return guard_patrol_map.get_traced_map()

def calculate_next_location(map_text):
    guard_patrol_map = GuardPatrolMap(map_text)
    return guard_patrol_map.next_guard_location()

def calculate_path(map_text):
    # Assuming calculate_path should provide a similar functionality as get_traced_map,
    # as the original implementation does not specify the path calculation.
    # For illustrative purposes, we will return the traced map.
    guard_patrol_map = GuardPatrolMap(map_text)
    return guard_patrol_map.get_traced_map()

def find_start_position(map_text):
    guard_patrol_map = GuardPatrolMap(map_text)
    return guard_patrol_map.find_guard()
