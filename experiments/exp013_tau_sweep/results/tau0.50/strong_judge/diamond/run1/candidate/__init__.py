def generate_alphabet_diamond(letter):
    if len(letter) != 1 or not letter.isalpha() or not letter.isupper():
        raise Exception("Input must be a single letter A-Z")

    N = ord(letter) - ord('A') + 1
    diamond = []

    # Create the upper half of the diamond
    for i in range(N):
        spaces = ' ' * (N - i - 1)
        if i == 0:
            row = f'{spaces}A'
        else:
            row = f'{spaces}{letter[i]} {' ' * (2 * i - 1)}{letter[i]}'
        diamond.append(row)

    # Create the lower half of the diamond
    for i in range(N - 2, -1, -1):
        spaces = ' ' * (N - i - 1)
        if i == 0:
            row = f'{spaces}A'
        else:
            row = f'{spaces}{letter[i]} {' ' * (2 * i - 1)}{letter[i]}'
        diamond.append(row)

    return '\n'.join(diamond)