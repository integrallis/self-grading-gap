def wrap_text(text, width):
    if text is None or text.strip() == '':
        return []

    lines = []
    current_line = ''

    for char in text:
        if char == '\n':
            if current_line:
                lines.append(current_line.rstrip())
                current_line = ''
            lines.append('')  # Insert a blank line for the line break
        elif char == ' ':
            if len(current_line) > 0 and len(current_line) + 1 < width:
                current_line += ' '
            elif len(current_line) >= width:
                lines.append(current_line.rstrip())
                current_line = ''
        else:
            if len(current_line) < width:
                current_line += char
            else:
                # We need to break the word
                if current_line:
                    lines.append(current_line.rstrip())
                # Start new line with the current char broken
                current_line = char

    if current_line:
        lines.append(current_line.rstrip())

    # Trim trailing spaces and filter out empty lines
    return [line for line in lines if line.strip() != '']