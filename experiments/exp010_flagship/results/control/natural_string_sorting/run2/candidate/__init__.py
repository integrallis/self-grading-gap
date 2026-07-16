import re

def sort_natural(items, descending=False):
    def natural_key(s):
        parts = re.split('([0-9]+)', s)
        return [(int(text) if text.isdigit() else text.lower()) for text in parts]

    return sorted(items, key=natural_key, reverse=descending)