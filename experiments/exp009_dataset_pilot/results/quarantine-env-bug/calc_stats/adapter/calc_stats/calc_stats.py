# file: calc_stats/calc_stats.py

from candidate.impl import NumberStatistics
from enum import Enum

class StatisticType(Enum):
    MINIMUM = "minimum"
    MAXIMUM = "maximum"
    COUNT = "count"
    AVERAGE = "average"

class CalcStats:
    def __init__(self, numbers):
        self._stats = NumberStatistics(numbers)

    def compute_statistic(self, statistic_type):
        return self._stats.compute_statistic(statistic_type.value)
