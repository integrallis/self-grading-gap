import re

def natural_key(s):
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]

def sort_strings_naturally(strings, descending=False):
    return sorted(strings, key=natural_key, reverse=descending)