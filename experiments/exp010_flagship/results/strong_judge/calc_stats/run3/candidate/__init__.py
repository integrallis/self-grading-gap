def compute_statistic(numbers, selector):
    if selector == "minimum":
        return str(min(numbers))
    elif selector == "maximum":
        return str(max(numbers))
    elif selector == "element count":
        return str(len(numbers))
    elif selector == "average":
        return str(sum(numbers) / len(numbers))
    else:
        return ""