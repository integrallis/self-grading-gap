# file: advent_day6/pathfinding.py
from candidate.impl import GuardPatrolMap


def calculate_grid(map_text):
    return GuardPatrolMap(map_text).grid


def calculate_next_location(map_text):
    return GuardPatrolMap(map_text).next_guard_location()


def calculate_path(map_text):
    return GuardPatrolMap(map_text).get_traced_map()


def find_start_position(map_text):
    return GuardPatrolMap(map_text).find_guard_position()
