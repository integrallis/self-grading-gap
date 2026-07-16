def add_numbers_from_text(text):
    if not text:
        return 0

    # Handle custom delimiter
    if text.startswith('//'):
        delimiter_part, numbers_part = text.split('\n', 1)
        delimiter = delimiter_part[2:]
    else:
        delimiter = ','
        numbers_part = text

    # Replace newlines with commas for proper parsing
    numbers_part = numbers_part.replace('\n', ',')

    # Replace custom delimiters with commas
    for char in delimiter:
        numbers_part = numbers_part.replace(char, ',')

    # Split the string by commas and convert to integers
    numbers = numbers_part.split(',')
    total = 0
    for number in numbers:
        if number:
            num = int(number.strip())  # Strip whitespace
            if num < 0:
                raise ValueError(f"string contains {num}, which does not meet rule. entered number should not negative.")
            if num <= 1000:
                total += num
    return total