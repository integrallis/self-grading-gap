def read_term(term):
    if not term or not term.isdigit():
        raise ValueError("term must be a non-empty string of digits")

    result = []
    count = 0
    for i in range(len(term)):
        count += 1
        if i == len(term) - 1 or term[i] != term[i + 1]:
            result.append(f'{count}{term[i]}')
    
    return ''.join(result)

def iterate(term, iterations):
    if iterations < 0:
        raise ValueError("iterations must be non-negative")
    if not term or not term.isdigit():
        raise ValueError("term must be a non-empty string of digits")

    for _ in range(iterations):
        term = read_term(term)
    return term
