'''The solution package.'''

__version__ = "0.1.0"

def render_digit(digit):
    patterns = [
        ["._.", "|.|", "|_|"],  # 0
        ["...", "..|", "..|"],  # 1
        ["._.", "._|", "|_|"] ,  # 2
        ["._.", "._|", "._|"] ,  # 3
        [...], # 4
        [...], # 5
        [...], # 6
        [...], # 7
        [...], # 8
        [...], # 9
    ]
    return '\n'.join(patterns[digit]) + '\n'

def render_number(number):
    digits = [int(d) for d in str(number)]
    rows = ["", "", ""]
    for digit in digits:
        digit_render = render_digit(digit).splitlines()
        for i in range(3):
            rows[i] += digit_render[i]
    return '\n'.join(rows) + '\n'