def check_bookended_text(text):
    if len(text) < 2:
        return False
    if len(text) == 3:
        return text[0] == text[-1]
    return text[:2] == text[-2:]