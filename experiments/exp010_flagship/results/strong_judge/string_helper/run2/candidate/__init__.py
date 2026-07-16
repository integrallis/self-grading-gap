def match_bookended_text(text):
    if len(text) < 2:
        return False
    start = text[:2]
    end = text[-2:]
    return start == end