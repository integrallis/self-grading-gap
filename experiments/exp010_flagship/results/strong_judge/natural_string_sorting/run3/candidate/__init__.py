def sort_mixed_text(input_data, descending=False):
    import re

    def sort_key(s):
        # Normalize whitespace and split the string into parts: digits and non-digits
        normalized = re.sub(r'\s+', '', s)
        parts = re.split(r'([0-9]+)', normalized)
        # Convert digit parts to integers for natural sorting
        return [(int(part) if part.isdigit() else part) for part in parts]

    # Sort the input data using the custom sort key
    sorted_data = sorted(input_data, key=sort_key)
    # Reverse if descending order is requested
    if descending:
        sorted_data.reverse()
    return sorted_data
