def sort_natural(input_data, descending=False):
    import re
    def natural_key(s):
        # Split the string into segments of digits and non-digits
        return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]

    # Sort the data using the natural key
    sorted_data = sorted(input_data, key=natural_key)
    # Reverse if descending order is requested
    if descending:
        sorted_data = sorted_data[::-1]
    return sorted_data
