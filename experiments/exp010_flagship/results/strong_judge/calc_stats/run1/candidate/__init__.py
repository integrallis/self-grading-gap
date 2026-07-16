def statistic_reporter(numbers, statistic):
    if statistic == "minimum":
        return str(min(numbers))
    elif statistic == "maximum":
        return str(max(numbers))
    elif statistic == "element count":
        return str(len(numbers))
    elif statistic == "average":
        return str(sum(numbers) / len(numbers))
    else:
        return ""