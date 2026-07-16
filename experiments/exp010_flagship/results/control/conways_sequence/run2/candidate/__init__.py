def read_term(term):
    if not term or not term.isdigit():
        raise ValueError("term must be a non-empty string of digits")
    result = []
    count = 1
    for i in range(1, len(term)):
        if term[i] == term[i - 1]:
            count += 1
        else:
            result.append(str(count) + term[i - 1])
            count = 1
    result.append(str(count) + term[-1])
    return ''.join(result)


def iterate_from_seed(seed, iterations):
    if iterations < 0:
        raise ValueError("iterations must be non-negative")
    if not seed or not seed.isdigit():
        raise ValueError("term must be a non-empty string of digits")
    term = seed
    for _ in range(iterations):
        term = read_term(term)
    return term