# candidate/impl.py

class NumberListStatistics:
    def __init__(self, numbers):
        if not all(isinstance(n, (int, float)) for n in numbers):
            raise ValueError("All elements in the list must be numbers.")
        self.numbers = numbers

    def compute_statistic(self, statistic):
        if statistic == 'minimum':
            return str(min(self.numbers))
        elif statistic == 'maximum':
            return str(max(self.numbers))
        elif statistic == 'count':
            return str(len(self.numbers))
        elif statistic == 'average':
            return str(sum(self.numbers) / len(self.numbers))
        else:
            return ""

# Example usage:
# stats = NumberListStatistics([1, -1, 2, -2, 6, 9, 15, -2, 92, 11])
# print(stats.compute_statistic('minimum'))  # Output: "-2"
# print(stats.compute_statistic('maximum'))  # Output: "92"
# print(stats.compute_statistic('count'))     # Output: "10"
# print(stats.compute_statistic('average'))   # Output: "13.1"
# print(stats.compute_statistic('unknown'))    # Output: ""
