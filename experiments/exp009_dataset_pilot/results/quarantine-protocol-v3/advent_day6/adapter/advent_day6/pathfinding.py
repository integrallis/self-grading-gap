# file: advent_day6/pathfinding.py
from candidate.impl import GuardPatrolMap as _GuardPatrolMap


def calculate_grid(map_text):
    return _GuardPatrolMap(map_text).parse_grid(map_text)


def calculate_next_location(map_text):
    return _GuardPatrolMap(map_text).get_next_location()


def calculate_path(map_text):
    return _GuardPatrolMap(map_text).get_traced_map()


def find_start_position(map_text):
    return _GuardPatrolMap(map_text).find_guard_position()
