def sort_natural(input_data, descending=False):
    import re
    def natural_key(s):
        # Split the string into components of numbers and letters
        parts = re.split('([0-9]+)', s)
        # Convert numeric parts to integers, keep text as is
        return [(int(part) if part.isdigit() else part) for part in parts]
    # Sort the input data with the natural key and handle descending order
    return sorted(input_data, key=natural_key, reverse=descending)
