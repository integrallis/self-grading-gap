'''The solution package.'''

__version__ = "0.1.0"

def matches_opening_closing_pairs(text):
    if len(text) < 2:
        return False
    opening = text[:2]
    closing = text[-2:]
    return opening == closing