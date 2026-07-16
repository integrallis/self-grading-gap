# candidate/impl.py

class NumberListStatistics:
    def __init__(self, numbers):
        self.numbers = numbers

    def compute_statistic(self, stat_type):
        if stat_type == 'minimum':
            return str(min(self.numbers))
        elif stat_type == 'maximum':
            return str(max(self.numbers))
        elif stat_type == 'count':
            return str(len(self.numbers))
        elif stat_type == 'average':
            return str(sum(self.numbers) / len(self.numbers)) if self.numbers else '0.0'
        else:
            return ''
