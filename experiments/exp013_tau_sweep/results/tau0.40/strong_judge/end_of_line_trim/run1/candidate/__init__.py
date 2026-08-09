import re

def trailing_whitespace_cleaner(text: str) -> str:
    return re.sub(r'[ \t]+(?=\r?\n|$)', '', text)