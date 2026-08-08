def compute_statistic(numbers, statistic_type):
    if statistic_type == 'minimum':
        return str(min(numbers))
    elif statistic_type == 'maximum':
        return str(max(numbers))
    elif statistic_type == 'count':
        return str(len(numbers))
    elif statistic_type == 'average':
        return str(sum(numbers) / len(numbers))
    else:
        return ""