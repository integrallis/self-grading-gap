def compute_statistic(data, statistic_type):
    if statistic_type == 'minimum':
        return str(min(data))
    elif statistic_type == 'maximum':
        return str(max(data))
    elif statistic_type == 'element count':
        return str(len(data))
    elif statistic_type == 'average':
        return str(sum(data) / len(data))
    else:
        return ""