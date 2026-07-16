def trailing_whitespace_cleaner(text: str) -> str:
    lines = text.splitlines(keepends=True)  # Split the input text into lines while keeping line endings
    cleaned_lines = []
    for line in lines:
        cleaned_line = line.rstrip(' \t')  # Remove trailing spaces and tabs from each line
        if cleaned_line and cleaned_line != '\n' and cleaned_line != '\r\n':  # If line is not just a newline
            cleaned_lines.append(cleaned_line)  # Append cleaned line if not empty
        else:
            cleaned_lines.append(line[-1])  # Append just the line ending for empty or whitespace-only lines
    return ''.join(cleaned_lines)  # Join cleaned lines back into a single string