def wrap_text(text, width):
    if text.strip() == "":
        return ""

    lines = []
    current_line = []
    current_length = 0

    i = 0
    while i < len(text):
        char = text[i]

        if char == '\n':
            if current_line:
                lines.append(' '.join(current_line))
                current_line = []
                current_length = 0
            lines.append('\n')
            i += 1
            continue

        if char == ' ':
            if current_line:
                lines.append(' '.join(current_line))
                current_line = []
                current_length = 0
            while i < len(text) and text[i] == ' ':
                i += 1
            continue

        word_start = i
        while i < len(text) and text[i] != ' ' and text[i] != '\n':
            i += 1
        word = text[word_start:i]

        word_length = len(word)

        if current_length + len(current_line) + word_length <= width:
            current_line.append(word)
            current_length += word_length + (1 if current_line else 0)
        else:
            while len(word) > width:
                lines.append(word[:width])
                word = word[width:]
            if word:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = []
                    current_length = 0
                current_line.append(word)
                current_length += len(word)

    if current_line:
        lines.append(' '.join(current_line))

    return ''.join(lines).rstrip()