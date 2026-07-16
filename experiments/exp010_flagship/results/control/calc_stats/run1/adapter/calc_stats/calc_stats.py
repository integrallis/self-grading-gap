# file: calc_stats/calc_stats.py
from candidate import compute_statistic


class CalcStats:
    @staticmethod
    def number_stats(numbers, statistic):
        return compute_statistic(numbers, getattr(statistic, "value", statistic))
