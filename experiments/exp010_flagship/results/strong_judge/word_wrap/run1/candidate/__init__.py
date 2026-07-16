def wrap_text(text: str, width: int) -> str:
    if not text.strip():
        return ""

    lines = []
    current_line = []

    for line in text.splitlines(keepends=True):
        for word in line.split(' '):
            # Process long words
            while len(word) > width:
                lines.append(word[:width])
                word = word[width:]
            # Check if we can add the word to the current line
            if current_line and len(' '.join(current_line)) + len(word) + 1 > width:
                lines.append(' '.join(current_line))
                current_line = []
            # Append the word to the current line
            if word:
                current_line.append(word)
        # Add the current line to the lines list if it's not empty
        if current_line:
            lines.append(' '.join(current_line))
            current_line = []

    return ''.join(lines).replace(' \n', '\n')