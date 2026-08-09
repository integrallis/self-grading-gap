def max_of_two(a, b):
    return max(a, b)

def max_of_one(a):
    return a

def max_of_any(*args):
    if not args:
        raise Exception("Function requires arguments")
    return max(args)

def max_of_at_least_one(first, *args):
    return max((first,) + args)

def always_refuses():
    raise TypeError("Function requires arguments")

def max_within_bounds(*args, low, high):
    valid_numbers = [x for x in args if low <= x <= high]
    return max(valid_numbers) if valid_numbers else low

def make_bounded_finder(low, high):
    def bounded_finder(*args):
        return max_within_bounds(*args, low=low, high=high)
    return bounded_finder