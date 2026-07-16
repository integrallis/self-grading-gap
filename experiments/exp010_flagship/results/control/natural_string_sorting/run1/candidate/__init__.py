def natural_sort(items, descending=False):
    import re
    key = lambda x: [int(text) if text.isdigit() else text.lower() for text in re.split('(?<=\D)(?=\d)|(?<=\d)(?=\D)', x.strip())]
    return sorted(items, key=key, reverse=descending)