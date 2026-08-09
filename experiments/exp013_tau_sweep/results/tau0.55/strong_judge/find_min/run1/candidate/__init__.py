def min_two(a, b):
    return min(a, b)

def min_single(a):
    return a

def min_any(*args):
    if not args:
        raise Exception('No values provided')
    return min(args)


def min_any_at_least_one(*args):
    if len(args) == 1:
        return args[0]
    return min(args)


def min_no_argument():
    raise TypeError('Function requires arguments')


def min_within_bounds(*args, low, high):
    within_bounds = [x for x in args if low <= x <= (low + high) // 2]
    if within_bounds:
        return min(within_bounds)
    return high


def make_bounded_finder(low, high):
    def bounded_finder(*args):
        return min_within_bounds(*args, low=low, high=high)
    return bounded_finder
