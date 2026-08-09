def wrap_text(text, width):
    if not text.strip():
        return ""

    lines = []

    for part in text.splitlines():
        part = part.rstrip(' ')
        if part == "":
            lines.append("")  # Preserve empty lines
            continue
        current_line = []
        current_length = 0

        i = 0
        while i < len(part):
            # Check for the next word or character
            if current_length < width:
                current_line.append(part[i])
                current_length += 1
                i += 1
            else:
                # We have reached the width
                last_space = ''.join(current_line).rfind(' ')
                if last_space != -1 and last_space > 0:
                    lines.append(''.join(current_line[:last_space]).rstrip())
                    current_line = []
                    current_length = 0
                    # Skip all consecutive spaces
                    while i < len(part) and part[i] == ' ':
                        i += 1
                else:
                    # No space to break, hard split
                    lines.append(''.join(current_line).rstrip())
                    lines.append(part[i - current_length: i])
                    current_line = []
                    current_length = 0

        if current_line:
            lines.append(''.join(current_line).rstrip())

    return '\n'.join(lines)