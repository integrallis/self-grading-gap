def add_numbers(numbers):
    if not numbers:
        return 0

    # Handle custom delimiter
    if numbers.startswith('//'):
        delimiter, numbers = numbers[2:].split('\n', 1)
    else:
        delimiter = ','

    # Replace custom delimiter with active delimiter and split the string
    numbers = numbers.replace('\n', delimiter).split(delimiter)

    total = 0
    negatives = []
    for number in numbers:
        if number == "":
            continue
        num = int(number)
        if num < 0:
            negatives.append(num)
        elif num <= 1000:
            total += num

    if negatives:
        raise Exception(f"string contains {', '.join(map(str, negatives))}, which does not meet rule. entered number should not negative.")

    return total