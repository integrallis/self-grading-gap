# file: calc_stats/calc_stats.py
from enum import Enum

from candidate import compute_statistic


class CalcStats(Enum):
    MINIMUM = "minimum"
    MAXIMUM = "maximum"
    COUNT = "count"
    AVERAGE = "average"

    @staticmethod
    def number_stats(numbers, statistic):
        return compute_statistic(numbers, getattr(statistic, "value", statistic))
