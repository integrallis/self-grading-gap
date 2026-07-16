def wrap_text(text, width):
    if not text.strip():
        return []

    lines = []
    current_line = []
    for part in text.splitlines():
        # Handle leading newline
        if part == '':
            lines.append('')
            continue
        for word in part.split():
            if len(word) > width:
                while len(word) > width:
                    lines.append(word[:width])
                    word = word[width:]
            if sum(len(w) for w in current_line) + len(current_line) + len(word) > width:
                lines.append(' '.join(current_line))
                current_line = []
            current_line.append(word)
        if current_line:
            lines.append(' '.join(current_line))
            current_line = []
    return lines