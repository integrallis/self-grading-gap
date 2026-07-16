'''The solution package.'''

__version__ = "0.1.0"

def wrap_text(text, width):
    if not text.strip():  # Handle empty or whitespace-only text
        return ""

    lines = []  # To hold the wrapped lines
    current_line = []  # To build the current line

    for line in text.splitlines(keepends=True):  # Process each line independently
        current_length = 0  # Length of the current line
        index = 0  # Current index in the line

        while index < len(line):
            if line[index] == '\n':  # Handle line breaks
                if current_line:
                    lines.append(''.join(current_line))
                lines.append('')  # Preserve the line break
                current_line = []
                current_length = 0
                index += 1
                continue

            start_index = index
            while index < len(line) and line[index] != '\n':  # Read until line break
                index += 1

            segment = line[start_index:index]
            segment_length = len(segment)

            while segment_length > width:
                # Hard split for long words
                lines.append(segment[:width])
                segment = segment[width:]
                segment_length = len(segment)

            if current_length + segment_length > width:
                # Break at the last space if possible
                last_space_index = segment.rfind(' ', 0, width - current_length)
                if last_space_index != -1:
                    lines.append(''.join(current_line) + segment[:last_space_index])
                    lines.append(segment[last_space_index + 1:])
                    current_line = []
                    current_length = 0
                else:
                    # Hard split if no space is found
                    lines.append(''.join(current_line) + segment[:width])
                    segment = segment[width:]
                    current_line = []
                    current_length = 0

            if segment:
                # Add the remaining segment to the current line
                current_line.append(segment)
                current_length += segment_length

        if current_line:
            lines.append(''.join(current_line))  # Add remaining words after the line ends

    wrapped_text = ''.join(lines)  # Join all lines with a newline
    return wrapped_text
