def add_numbers_from_delimited_text(text):
    if not text:
        return 0

    # Check for custom delimiter
    if text.startswith("//"):
        delimiter_part = text.split('\n', 1)[0][2:]
        delimiter = delimiter_part.split("[\n]")[0]
        text = text.split('\n', 1)[1]
    else:
        delimiter = ','

    # Replace newlines with delimiter
    text = text.replace('\n', delimiter)

    # Split the input string into numbers
    numbers = text.split(delimiter)

    total = 0
    negatives = []
    for num in numbers:
        num = int(num)
        if num < 0:
            negatives.append(num)
        elif num <= 1000:
            total += num

    if negatives:
        raise ValueError(f"string contains {', '.join(map(str, negatives))}, which does not meet rule. entered number should not negative.")

    return total