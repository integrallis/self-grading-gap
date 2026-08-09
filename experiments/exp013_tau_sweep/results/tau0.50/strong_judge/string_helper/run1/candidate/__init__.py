def matches_opening_closing_pairs(text):
    if len(text) < 2:
        return False
    opening = text[:2]
    closing = text[-2:]
    return opening == closing or (opening[0] == opening[1] and closing[0] == closing[1])