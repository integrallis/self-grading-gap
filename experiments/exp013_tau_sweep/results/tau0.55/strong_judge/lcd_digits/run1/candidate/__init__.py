def render_digit(digit):
    segments = {
        '0': ['._.', '|.|', '|_|'],
        '1': ['...', '..|', '..|'],
    }
    # Create an empty display for the three rows
    rows = ['', '', '']
    for char in str(digit):
        if char in segments:
            for i in range(3):
                rows[i] += segments[char][i]
    # Join rows with a newline and add a trailing newline
    return '\n'.join(rows) + '\n'
