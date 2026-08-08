def wrap_text(text, width):
    if not text.strip():  # Handle empty or whitespace-only input
        return ""

    lines = []
    current_line = []
    current_length = 0

    for char in text:
        if char == '\n':  # Handle line breaks
            if current_line:
                lines.append(''.join(current_line))
                current_line = []
                current_length = 0
            lines.append('\n')  # Add the line break
            continue

        if char.isspace():  # Handle spaces
            if current_line:
                lines.append(''.join(current_line))  # Flush current line on space
                current_line = []
                current_length = 0
            continue

        if current_length == width:  # Hard split if at width
            lines.append(''.join(current_line))
            current_line = []
            current_length = 0

        if current_length + 1 > width:  # Check if adding this char exceeds width
            if current_line:
                lines.append(''.join(current_line))
                current_line = []
                current_length = 0
            # Hard split on long word
            for i in range(0, len(char), width):
                lines.append(char[i:i+width])
            continue

        current_line.append(char)
        current_length += 1

    if current_line:  # Append any remaining characters
        lines.append(''.join(current_line))

    return '\n'.join(lines)