def justify_text(text, width):
    if text is None:
        raise ValueError("text must not be None")
    if width <= 0:
        raise ValueError("width must be a positive integer")

    # Normalize whitespace
    words = ' '.join(text.split()).split() if text else []
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + len(current_line) > width:
            # Justify the current line
            if len(current_line) == 1:
                lines.append(current_line[0].ljust(width))
            else:
                total_spaces = width - sum(len(w) for w in current_line)
                spaces_between = len(current_line) - 1
                space_width = total_spaces // spaces_between
                extra_spaces = total_spaces % spaces_between
                line = ''
                for i, w in enumerate(current_line):
                    line += w
                    if i < spaces_between:
                        line += ' ' * (space_width + (1 if i < extra_spaces else 0))
                lines.append(line)
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)

    # Last line flush left
    if current_line:
        if len(current_line) == 1:
            lines.append(current_line[0].ljust(width))
        else:
            lines.append(' '.join(current_line))

    return lines
