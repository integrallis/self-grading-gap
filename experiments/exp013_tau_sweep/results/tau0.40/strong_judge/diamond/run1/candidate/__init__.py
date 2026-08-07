def generate_diamond(letter):
    letter = letter.upper()
    if len(letter) != 1 or not ('A' <= letter <= 'Z'):
        raise Exception("Input must be a single letter A-Z")

    N = ord(letter) - ord('A') + 1
    diamond = []

    # Create the upper part of the diamond
    for i in range(N):
        spaces = ' ' * (N - i - 1)
        if i == 0:
            diamond.append(f'{spaces}A')
        else:
            inner_spaces = ' ' * (2 * i - 1)
            diamond.append(f'{spaces}{chr(ord("A") + i)}{inner_spaces}{chr(ord("A") + i)}')

    # Create the lower part of the diamond
    for i in range(N - 2, -1, -1):
        diamond.append(diamond[i])

    return '\n'.join(diamond)