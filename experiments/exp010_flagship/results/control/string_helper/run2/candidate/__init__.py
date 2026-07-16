def matching_pairs(text):
    if len(text) < 2:
        return False
    elif len(text) >= 4 and text[:2] == text[-2:]:
        return True
    else:
        return False