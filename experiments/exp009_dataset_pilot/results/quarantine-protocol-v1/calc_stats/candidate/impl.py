# candidate/impl.py

class StatisticsReporter:
    def __init__(self, numbers):
        self.numbers = numbers

    def compute_statistic(self, statistic_type):
        if statistic_type == "minimum":
            return str(min(self.numbers))
        elif statistic_type == "maximum":
            return str(max(self.numbers))
        elif statistic_type == "count":
            return str(len(self.numbers))
        elif statistic_type == "average":
            return str(sum(self.numbers) / len(self.numbers)) if self.numbers else "0.0"
        else:
            return ""

# Example usage:
# reporter = StatisticsReporter([1, -1, 2, -2, 6, 9, 15, -2, 92, 11])
# print(reporter.compute_statistic("minimum"))  # "-2"
# print(reporter.compute_statistic("maximum"))  # "92"
# print(reporter.compute_statistic("count"))     # "10"
# print(reporter.compute_statistic("average"))   # "13.1"
# print(reporter.compute_statistic("unknown"))   # ""
