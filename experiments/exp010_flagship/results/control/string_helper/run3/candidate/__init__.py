def check_bookended(text):
    if len(text) < 2:
        return False
    return text[:2] == text[-2:]