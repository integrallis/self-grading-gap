def justify_text(text, width):
    if text is None:
        raise ValueError("text must not be None")
    if not isinstance(width, int) or width <= 0:
        raise ValueError("width must be a positive integer")

    words = text.split()  # Split the text into words, handling multiple spaces
    lines = []  # List to hold the justified lines
    current_line = []  # List to hold words for the current line
    current_length = 0  # Current length of words in the current line

    for word in words:
        word_length = len(word)
        # Check if adding this word exceeds the width
        if current_length + len(current_line) + word_length > width:
            if current_line:
                # If it does, justify the current line
                for i in range(width - current_length):
                    # Add spaces to the current line
                    current_line[i % (len(current_line) - 1 or 1)] += ' '
                lines.append(''.join(current_line))
            current_line = [word]  # Start a new line with the current word
            current_length = word_length
        else:
            current_line.append(word)  # Add the word to the current line
            current_length += word_length

    # Handle the last line, flush left
    if current_line:
        lines.append(' '.join(current_line))

    return lines
