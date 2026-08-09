import re

def clean_trailing_whitespace(text):
    return re.sub(r'[ \t]+(?=\r?\n|$)', '', text)