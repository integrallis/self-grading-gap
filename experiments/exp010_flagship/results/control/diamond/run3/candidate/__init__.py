def generate_alphabet_diamond(letter):
    if len(letter) != 1 or not letter.isalpha() or not (letter.isupper() or letter.islower()):
        raise ValueError("Input must be a single letter A-Z")
    n = ord(letter.upper()) - ord('A')
    diamond = []

    # Create the upper part including the middle line
    for i in range(n + 1):
        line = ' ' * (n - i) + chr(ord('A') + i)
        if i > 0:
            line += ' ' + chr(ord('A') + i) + ' '
        diamond.append(line)

    # Create the lower part
    for i in range(n - 1, -1, -1):
        line = ' ' * (n - i) + chr(ord('A') + i)
        if i > 0:
            line += ' ' + chr(ord('A') + i) + ' '
        diamond.append(line)

    return '\n'.join(diamond) + '\n'