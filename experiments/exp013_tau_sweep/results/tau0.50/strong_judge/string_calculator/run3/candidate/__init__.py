def add_numbers_from_text(text):
    if not text:
        return 0

    # Check for custom delimiter
    if text.startswith('//'):
        delimiter_end = text.index('\n')
        delimiter = text[2:delimiter_end]
        numbers_text = text[delimiter_end + 1:]
    else:
        delimiter = ','
        numbers_text = text

    # Replace newlines with delimiter
    numbers_text = numbers_text.replace('\n', delimiter)

    # Split numbers and convert to integers, while checking for negatives
    numbers = numbers_text.split(delimiter)
    total = 0
    for number in numbers:
        if number == "":
            continue
        num = int(number)
        if num < 0:
            raise Exception(f"string contains {num}, which does not meet rule. entered number should not negative.")
        if num <= 1000:
            total += num

    return total
