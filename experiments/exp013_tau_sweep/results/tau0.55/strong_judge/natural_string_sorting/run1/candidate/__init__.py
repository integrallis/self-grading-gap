def natural_sort(items, descending=False):
    import re
    def natural_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]
    sorted_items = sorted(items, key=natural_key, reverse=descending)
    return sorted_items