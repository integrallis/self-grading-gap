def add_numbers(numbers):
    if not numbers:
        return 0

    # Check for custom delimiter
    if numbers.startswith('//'):
        delimiter_part, numbers = numbers.split('\n', 1)
        delimiter = delimiter_part[2:]
    else:
        delimiter = ','

    # Replace custom delimiter and newlines with commas
    numbers = numbers.replace('\n', ',').replace(delimiter, ',')

    # Split the numbers and convert to integers
    num_list = numbers.split(',')

    total = 0
    for num in num_list:
        num = int(num)
        if num < 0:
            raise ValueError(f"string contains {num}, which does not meet rule. entered number should not negative.")
        if num <= 1000:
            total += num

    return total