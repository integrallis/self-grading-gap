def generate_alphabet_diamond(letter):
    if not isinstance(letter, str) or len(letter) != 1 or not letter.isalpha() or letter.upper() < 'A' or letter.upper() > 'Z':
        raise ValueError("Input must be a single letter A-Z")

    letter = letter.upper()
    n = ord(letter) - ord('A')
    diamond = []

    for i in range(n + 1):
        spaces = ' ' * (n - i)
        if i == 0:
            diamond.append(spaces + 'A' + spaces)
        else:
            diamond.append(spaces + chr(ord('A') + i) + ' ' * (2 * i - 1) + chr(ord('A') + i) + spaces)

    for i in range(n - 1, -1, -1):
        spaces = ' ' * (n - i)
        if i == 0:
            diamond.append(spaces + 'A' + spaces)
        else:
            diamond.append(spaces + chr(ord('A') + i) + ' ' * (2 * i - 1) + chr(ord('A') + i) + spaces)

    return '\n'.join(diamond)