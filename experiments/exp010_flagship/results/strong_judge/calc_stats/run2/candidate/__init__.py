def compute_statistic(numbers, statistic):
    if statistic == 'minimum':
        return str(min(numbers))
    elif statistic == 'maximum':
        return str(max(numbers))
    elif statistic == 'count':
        return str(len(numbers))
    elif statistic == 'average':
        return f'{sum(numbers) / len(numbers):.1f}'
    else:
        return ''
