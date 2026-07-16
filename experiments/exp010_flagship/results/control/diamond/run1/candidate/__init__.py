def generate_diamond(letter):
    if not (letter.isalpha() and len(letter) == 1 and letter.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        raise ValueError('Input must be a single letter A-Z')

    letter = letter.upper()
    n = ord(letter) - ord('A')
    diamond = []

    # Create the upper part of the diamond including the middle line
    for i in range(n + 1):
        spaces = ' ' * (n - i)
        if i == 0:
            diamond.append(spaces + 'A' + spaces)
        else:
            diamond.append(spaces + chr(ord('A') + i) + ' ' + chr(ord('A') + i) + spaces)

    # Create the lower part of the diamond
    for i in range(n - 1, -1, -1):
        spaces = ' ' * (n - i)
        if i == 0:
            diamond.append(spaces + 'A' + spaces)
        else:
            diamond.append(spaces + chr(ord('A') + i) + ' ' + chr(ord('A') + i) + spaces)

    return '\n'.join(diamond)