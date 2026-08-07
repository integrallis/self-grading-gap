'''The solution package.''' 

__version__ = "0.1.0"

def match_bookended_text(text):
    if len(text) < 2:
        return False
    return text[:2] == text[-2:]