def check_bookended_text(text):
    if len(text) < 2:
        return False
    opening = text[:2]
    closing = text[-2:]
    return opening == closing