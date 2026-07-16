# file: calc_stats/calc_stats.py
from candidate.impl import StatisticsReporter

class CalcStats:
    def __init__(self, numbers):
        self.reporter = StatisticsReporter(numbers)

    def compute_statistic(self, statistic_type):
        return self.reporter.compute_statistic(statistic_type)
