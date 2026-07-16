# file: calc_stats/calc_stats.py
from candidate.impl import NumberListStatistics


class CalcStats:
    @staticmethod
    def number_stats(numbers, stat_type):
        return NumberListStatistics(numbers).compute_statistic(stat_type.value)
