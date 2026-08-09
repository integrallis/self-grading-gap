def render_lcd(number):
    lcd_map = {
        '0': '._.\n|.|\n|_|',
        '1': '...\n..|\n..|',
        '2': '._.\n._|\n|_.',
        '3': '._.\n._|\n._|',
        '4': '...\n|_|\n..|',
        '5': '._.\n|_.\n._|',
        '6': '._.\n|_.\n|_|',
        '7': '._.\n..|\n..|',
        '8': '._.\n|_|\n|_|',
        '9': '._.\n|_|\n..|'
    }
    rows = ['', '', '']
    for digit in str(number):
        segments = lcd_map[digit].split('\n')
        for i in range(3):
            rows[i] += segments[i]
    return '\n'.join(rows) + '\n'