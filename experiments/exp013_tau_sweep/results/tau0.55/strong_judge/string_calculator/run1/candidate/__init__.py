def add_numbers(numbers):
    if not numbers:
        return 0

    # Check for custom delimiter
    if numbers.startswith('//'):
        delimiter, numbers = numbers[2:].split('\n', 1)
        delimiter = delimiter[0]  # Take the first character as delimiter
    else:
        delimiter = ','

    # Replace newlines with the delimiter
    numbers = numbers.replace('\n', delimiter)

    # Split the numbers and convert to integers
    num_list = numbers.split(delimiter)
    total = 0
    negatives = []

    for num in num_list:
        if num == '':
            continue
        number = int(num)
        if number < 0:
            negatives.append(number)
        elif number <= 1000:
            total += number

    if negatives:
        raise BaseException(f"string contains {','.join(map(str, negatives))}, which does not meet rule. entered number should not negative.")

    return total
