def matches_opening_closing_pairs(text):
    if len(text) < 2:
        return False
    first_pair = text[:2]
    last_pair = text[-2:]
    return first_pair == last_pair