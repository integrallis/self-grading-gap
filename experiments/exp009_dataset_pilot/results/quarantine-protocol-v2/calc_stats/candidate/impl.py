# candidate/impl.py

class StatisticsReporter:
    def __init__(self, numbers):
        self.numbers = numbers

    def compute_statistic(self, statistic):
        if statistic == "minimum":
            return str(min(self.numbers)) if self.numbers else ""
        elif statistic == "maximum":
            return str(max(self.numbers)) if self.numbers else ""
        elif statistic == "count":
            return str(len(self.numbers))
        elif statistic == "average":
            return str(sum(self.numbers) / len(self.numbers)) if self.numbers else ""
        else:
            return ""

# Example usage:
# reporter = StatisticsReporter([1, -1, 2, -2, 6, 9, 15, -2, 92, 11])
# print(reporter.compute_statistic("minimum"))  # Output: "-2"
# print(reporter.compute_statistic("maximum"))  # Output: "92"
# print(reporter.compute_statistic("count"))    # Output: "10"
# print(reporter.compute_statistic("average"))  # Output: "13.1"
# print(reporter.compute_statistic("unknown"))  # Output: ""
