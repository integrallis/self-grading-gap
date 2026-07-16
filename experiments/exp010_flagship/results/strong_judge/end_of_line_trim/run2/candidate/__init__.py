def trailing_whitespace_cleaner(text: str) -> str:
    lines = text.splitlines(keepends=True)
    cleaned_lines = []

    for line in lines:
        # Remove trailing whitespace but keep the line ending
        cleaned_line = line.rstrip(' \t')  # Remove spaces and tabs
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
        elif line.endswith('\n') or line.endswith('\r'):
            cleaned_lines.append('')  # Preserve empty line endings

    return ''.join(cleaned_lines)