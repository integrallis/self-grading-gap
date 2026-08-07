def read_term(term):
    if not term or not term.isdigit():
        raise Exception('term must be a non-empty string of digits')
    result = ''
    count = 1
    previous_char = term[0]
    for char in term[1:]:
        if char == previous_char:
            count += 1
        else:
            result += str(count) + previous_char
            previous_char = char
            count = 1
    result += str(count) + previous_char
    return result


def iterate_from_seed(seed, iterations):
    if iterations < 0:
        raise Exception('iterations must be non-negative')
    if not seed or not seed.isdigit():
        raise Exception('term must be a non-empty string of digits')
    current_term = seed
    for _ in range(iterations):
        current_term = read_term(current_term)
    return current_term
