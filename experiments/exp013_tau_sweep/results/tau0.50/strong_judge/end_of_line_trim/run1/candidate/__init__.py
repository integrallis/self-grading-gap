def clean_trailing_whitespace(text):
    lines = text.splitlines(keepends=True)
    cleaned_lines = []
    for line in lines:
        cleaned_line = line.rstrip(' \t')  # Remove trailing spaces and tabs
        # Preserve line endings by appending only cleaned line endings or empty lines
        if cleaned_line or (line.endswith(('\n', '\r')) and cleaned_line == ''):
            cleaned_lines.append(cleaned_line)
        else:
            cleaned_lines.append('')  # Preserve empty lines correctly
    return ''.join(cleaned_lines)