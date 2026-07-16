def sort_mixed_text(data, descending=False):
    def sort_key(s):
        prefix = s[0].isdigit()
        numeric_part = ''.join(filter(str.isdigit, s))
        return (not prefix, int(numeric_part) if numeric_part else float('inf'), s)
    sorted_data = sorted(data, key=sort_key, reverse=descending)
    return sorted_data
