def read_term(term):
    if not isinstance(term, str) or not term.isdigit() or not term:
        raise Exception("term must be a non-empty string of digits")
    result = []
    count = 1
    previous_char = term[0]
    for char in term[1:]:
        if char == previous_char:
            count += 1
        else:
            result.append(str(count) + previous_char)
            previous_char = char
            count = 1
    result.append(str(count) + previous_char)
    return ''.join(result)

def iterate_term(term, iterations):
    if iterations < 0:
        raise Exception("iterations must be non-negative")
    if not isinstance(term, str) or not term.isdigit() or not term:
        raise Exception("term must be a non-empty string of digits")
    for _ in range(iterations):
        term = read_term(term)
    return term
