def justify_text(text, width):
    if text is None:
        raise ValueError("text must not be None")
    if width <= 0:
        raise ValueError("width must be a positive integer")

    import re
    words = re.split(r'\s+', text.strip())
    if not words:
        return []

    result = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)
        if current_length + len(current_line) + word_length > width:
            result.append(justify_line(current_line, width))
            current_line = [word]
            current_length = word_length
        else:
            current_line.append(word)
            current_length += word_length

    if current_line:
        result.append(' '.join(current_line).rstrip())

    return result


def justify_line(line, width):
    if len(line) == 1:
        return line[0].ljust(width)
    total_spaces = width - sum(len(word) for word in line)
    spaces_between_words = len(line) - 1
    even_space = total_spaces // spaces_between_words
    extra_space = total_spaces % spaces_between_words

    justified_line = []
    for i, word in enumerate(line):
        justified_line.append(word)
        if i < spaces_between_words:
            justified_line.append(' ' * (even_space + (1 if i < extra_space else 0)))

    return ''.join(justified_line).rstrip()