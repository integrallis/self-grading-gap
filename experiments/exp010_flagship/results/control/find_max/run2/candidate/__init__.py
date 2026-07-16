def find_max(a, b):
    return max(a, b)


def find_max_single(value):
    return value


def find_max_any(*args):
    if not args:
        raise ValueError('No values provided')
    return max(args)


def find_max_at_least_one(*args):
    return max(args)


def find_max_within_bounds(low, high, *candidates):
    valid_candidates = [c for c in candidates if low <= c <= high]
    if not valid_candidates:
        return low
    return max(valid_candidates)


def manufacture_bounded_finder(low, high):
    def bounded_finder(*candidates):
        return find_max_within_bounds(low, high, *candidates)
    return bounded_finder


def always_refuses(*args):
    raise TypeError('Function requires arguments')