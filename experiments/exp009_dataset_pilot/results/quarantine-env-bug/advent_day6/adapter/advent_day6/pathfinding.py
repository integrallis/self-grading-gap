# file: advent_day6/pathfinding.py

from candidate.impl import GuardPatrolMap

def calculate_grid(map_text):
    guard_patrol_map = GuardPatrolMap(map_text)
    return guard_patrol_map.get_traced_map()

def calculate_next_location(map_text):
    guard_patrol_map = GuardPatrolMap(map_text)
    return guard_patrol_map.next_guard_location()

def calculate_path(map_text):
    guard_patrol_map = GuardPatrolMap(map_text)
    guard_patrol_map.trace_guard_walk()
    return guard_patrol_map.get_traced_map()

def find_start_position(map_text):
    guard_patrol_map = GuardPatrolMap(map_text)
    return guard_patrol_map.locate_guard()
