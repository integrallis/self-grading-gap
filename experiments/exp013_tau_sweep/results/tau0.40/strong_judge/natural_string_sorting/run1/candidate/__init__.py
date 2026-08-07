import re

def sort_mixed_text(data, descending=False):
    def natural_key(s):
        # Split the string into parts of digits and non-digits
        parts = re.split('([0-9]+)', s)
        # Convert digit parts to integers for proper comparison
        return [(int(part) if part.isdigit() else part) for part in parts if part]

    # Sort the data using the natural key and the descending flag
    return sorted(data, key=natural_key, reverse=descending)