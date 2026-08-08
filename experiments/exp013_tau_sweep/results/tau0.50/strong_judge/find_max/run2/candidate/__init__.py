def find_largest_two(a, b):
    return max(a, b)

def find_largest_single(value):
    return value

def find_largest_any(*args):
    if not args:
        raise Exception()
    return max(args)

def find_largest_at_least_one(*args):
    return max(args)

def find_largest_within_bounds(*args, low, high):
    in_bounds = [x for x in args if low <= x <= high]
    return max(in_bounds) if in_bounds else low

def create_bounded_finder(low, high):
    def bounded_finder(*args):
        return find_largest_within_bounds(*args, low=low, high=high)
    return bounded_finder

def always_refuse(*args):
    raise TypeError('Function requires arguments')