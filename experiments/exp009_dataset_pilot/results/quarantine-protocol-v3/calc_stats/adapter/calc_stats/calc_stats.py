# file: calc_stats/calc_stats.py
from candidate.impl import NumberListStatistics


class CalcStats:
    def number_stats(self, numbers, statistic):
        return NumberListStatistics(numbers).compute_statistic(statistic.value)
