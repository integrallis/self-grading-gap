def text_wrap(text, width):
    if not text.strip():
        return ""

    lines = []

    for line in text.splitlines():
        if len(line) == 0:
            lines.append("")  # Preserve empty lines
            continue

        index = 0
        current_line = []
        current_length = 0

        while index < len(line):
            char = line[index]

            if char == ' ':
                if current_length == width:
                    lines.append(''.join(current_line))
                    current_line = []
                    current_length = 0
                elif current_length > 0:
                    current_line.append(char)
                    current_length += 1
                    index += 1
                else:
                    index += 1
                    continue

            elif char == '\t':
                if current_length == width:
                    lines.append(''.join(current_line))
                    current_line = []
                    current_length = 0
                else:
                    current_line.append(char)
                    current_length += 1
                    index += 1

            else:
                if current_length < width:
                    current_line.append(char)
                    current_length += 1
                    index += 1
                else:
                    if current_line:
                        lines.append(''.join(current_line))
                    if current_length == 0:
                        lines.append(line[index:index + width])
                        index += width
                    else:
                        last_space_index = ''.join(current_line).rfind(' ')
                        if last_space_index != -1:
                            lines.append(''.join(current_line[:last_space_index]))
                            current_line = [char]
                            current_length = len(current_line)
                        else:
                            lines.append(''.join(current_line))
                            current_line = []
                            current_length = 0

        if current_line:
            lines.append(''.join(current_line))

    return '\n'.join(lines)