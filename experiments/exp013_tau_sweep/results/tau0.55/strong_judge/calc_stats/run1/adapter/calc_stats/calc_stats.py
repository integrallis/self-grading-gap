# file: calc_stats/calc_stats.py
from enum import Enum

from candidate import compute_statistic


class CalcStats(Enum):
    MINIMUM = "minimum"
    MAXIMUM = "maximum"
    COUNT = "count"
    AVERAGE = "average"

    @staticmethod
    def number_stats(numbers, selector):
        return compute_statistic(numbers, selector.value)
