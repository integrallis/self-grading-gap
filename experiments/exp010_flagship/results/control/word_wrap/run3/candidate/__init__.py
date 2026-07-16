def wrap_text(text, width):
    if not text.strip():
        return []
    lines = []
    current_line = []
    current_length = 0
    
    for part in text.splitlines():
        if part == '':
            lines.append('')  # Preserve empty lines
            continue
        position = 0
        while position < len(part):
            if part[position] == ' ':
                position += 1  # Skip spaces
                continue
            start = position
            # Move position to the end of the current word
            while position < len(part) and part[position] != ' ':
                position += 1
            word = part[start:position]
            word_length = len(word)
            
            if current_length + len(current_line) + word_length > width:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = []
                current_length = 0
            current_line.append(word)
            current_length += word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        current_line = []
        current_length = 0
    
    # Final formatting to ensure hard breaks are respected
    final_lines = []
    for line in lines:
        while len(line) > width:
            final_lines.append(line[:width])
            line = line[width:]  # Consume the line up to width
        if line:
            final_lines.append(line)
    
    # Clean up to avoid consuming leading spaces or tabs
    cleaned_lines = []
    for line in final_lines:
        if line and line[-1] == ' ':
            line = line.rstrip()  # Remove trailing spaces
        cleaned_lines.append(line)

    return cleaned_lines