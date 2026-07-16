# file: calc_stats/calc_stats.py
from candidate import compute_statistic


class CalcStats:
    @staticmethod
    def number_stats(numbers, selector):
        return compute_statistic(numbers, getattr(selector, "value", selector))
