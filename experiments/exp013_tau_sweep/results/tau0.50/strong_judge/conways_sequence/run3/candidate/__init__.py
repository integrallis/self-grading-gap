def read_term(term):
    if not term or not term.isdigit():
        raise Exception('term must be a non-empty string of digits')
    result = []
    count = 1
    for i in range(1, len(term)):
        if term[i] == term[i - 1]:
            count += 1
        else:
            result.append(str(count))
            result.append(term[i - 1])
            count = 1
    result.append(str(count))
    result.append(term[-1])
    return ''.join(result)


def iterate(term, iterations):
    if iterations < 0:
        raise Exception('iterations must be non-negative')
    if not term or not term.isdigit():
        raise Exception('term must be a non-empty string of digits')
    for _ in range(iterations):
        term = read_term(term)
    return term
