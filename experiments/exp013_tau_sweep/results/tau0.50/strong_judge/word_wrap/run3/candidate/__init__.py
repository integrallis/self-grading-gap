def wrap_text(text, width):
    if not text.strip():
        return ""
    lines = []
    current_line = []
    current_length = 0

    for part in text.splitlines():
        if part == '':
            lines.append('')  # Preserve empty lines
            continue
        words = part.split(' ')
        for word in words:
            # Check if adding the next word exceeds the width
            if current_length + len(word) + (1 if current_line else 0) > width:
                lines.append(' '.join(current_line))
                current_line = []
                current_length = 0
            # Handle long words
            if len(word) > width:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = []
                    current_length = 0
                for i in range(0, len(word), width):
                    lines.append(word[i:i + width])
                continue
            # Add the word to the current line
            if word:
                current_line.append(word)
                current_length += len(word) + (1 if current_line else 0)
        if current_line:
            lines.append(' '.join(current_line))
            current_line = []
            current_length = 0

    return '\n'.join(lines)