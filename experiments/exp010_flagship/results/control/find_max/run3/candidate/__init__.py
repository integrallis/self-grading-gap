def find_largest(*args):
    return max(args)

def find_largest_any(*args):
    if not args:
        raise ValueError("Cannot find largest of empty input")
    return max(args)

def find_largest_at_least_one(*args):
    return max(args)

def find_largest_within_bounds(low, high, *candidates):
    valid_candidates = [x for x in candidates if low <= x <= high]
    return max(valid_candidates) if valid_candidates else low

def make_bounded_finder(low, high):
    def bounded_finder(*candidates):
        return find_largest_within_bounds(low, high, *candidates)
    return bounded_finder

def always_refuses(*args):
    raise TypeError("Function requires arguments")