def compute_statistic(numbers, selector):
    if selector == "minimum":
        return str(min(numbers))
    elif selector == "maximum":
        return str(max(numbers))
    elif selector == "count":
        return str(len(numbers))
    elif selector == "average":
        return str(round(sum(numbers) / len(numbers), 1))
    else:
        return ""