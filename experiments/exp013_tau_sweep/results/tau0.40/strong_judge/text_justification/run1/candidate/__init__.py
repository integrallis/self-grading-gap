def justify_text(text, width):
    if text is None:
        raise Exception("text must not be None")
    if not isinstance(width, int) or width <= 0:
        raise Exception("width must be a positive integer")

    words = list(filter(None, text.split()))  # Split by whitespace and remove empty entries
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)
        if word_length > width:
            if current_line:
                lines.append(current_line)
                current_line = []
                current_length = 0
            lines.append([word])  # Oversized word goes on its own line
        else:
            if current_length + len(current_line) + word_length > width:
                lines.append(current_line)
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length

    if current_line:
        lines.append(current_line)  # Add the last line

    justified_lines = []
    for i in range(len(lines)):
        line = lines[i]
        if i == len(lines) - 1:  # Last line, flush left
            justified_lines.append(' '.join(line))
        else:
            total_chars = sum(len(word) for word in line)
            total_spaces = width - total_chars
            gaps = len(line) - 1
            if gaps > 0:
                spaces_per_gap = total_spaces // gaps
                extra_spaces = total_spaces % gaps
                justified_line = ''
                for j in range(gaps):
                    justified_line += line[j]  # Add word
                    justified_line += ' ' * (spaces_per_gap + (1 if j < extra_spaces else 0))  # Add spaces
                justified_line += line[-1]  # Add last word
                justified_lines.append(justified_line)
            else:
                justified_lines.append(line[0] + ' ' * total_spaces)  # Single word line

    return justified_lines