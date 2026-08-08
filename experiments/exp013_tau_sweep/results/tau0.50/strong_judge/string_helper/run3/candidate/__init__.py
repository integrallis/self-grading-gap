def matching_opening_closing_pairs(text):
    if len(text) < 2:
        return False
    return text[:2] == text[-2:]