'''The solution package.'''

__version__ = "0.1.0"

def make_change(amount):
    denominations = [25, 10, 5, 1]
    change = []
    for denomination in denominations:
        while amount >= denomination:
            change.append(denomination)
            amount -= denomination
    return change