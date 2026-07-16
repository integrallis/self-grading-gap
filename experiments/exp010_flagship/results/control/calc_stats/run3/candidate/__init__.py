def compute_statistic(data, statistic):
    if statistic == "minimum":
        return str(min(data))
    elif statistic == "maximum":
        return str(max(data))
    elif statistic == "count":
        return str(len(data))
    elif statistic == "average":
        return str(sum(data) / len(data))
    else:
        return ""