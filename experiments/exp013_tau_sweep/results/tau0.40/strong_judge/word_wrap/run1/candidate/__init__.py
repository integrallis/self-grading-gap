def wrap_text(text, width):
    lines = []
    current_line = []
    current_length = 0
    i = 0
    while i < len(text):
        char = text[i]
        if char == '\n':
            if current_line:
                lines.append(''.join(current_line))
                current_line = []
                current_length = 0
            lines.append('\n')
            i += 1
            continue
        elif char == ' ':
            if current_length > 0:
                current_line.append(' ')
                current_length += 1
            i += 1
            continue
        elif char == '\t':
            if current_length + 1 <= width:
                current_line.append('\t')
                current_length += 1
            i += 1
            continue
        # For non-whitespace characters
        if current_length + 1 > width:
            if current_line:
                lines.append(''.join(current_line))
                current_line = []
                current_length = 0
        current_line.append(char)
        current_length += 1
        i += 1

    if current_line:
        lines.append(''.join(current_line))
    result = ''.join(lines).rstrip(' ')
    return result.replace('\\n', '\n')