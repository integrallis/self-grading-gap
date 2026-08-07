def find_largest_two(a, b):
    return max(a, b)

def find_largest_single(a):
    return a

def find_largest_any(*args):
    if not args:
        raise Exception("No values provided")
    return max(args)

def find_largest_at_least_one(*args):
    if not args:
        raise Exception("At least one value required")
    return max(args)

def find_largest_within_bounds(*args, low, high):
    valid_numbers = [x for x in args if low <= x <= high]
    return max(valid_numbers) if valid_numbers else low

def make_bounded_finder(low, high):
    def bounded_finder(*args):
        return find_largest_within_bounds(*args, low=low, high=high)
    return bounded_finder

def always_refuses(*args):
    raise TypeError("Function requires arguments")