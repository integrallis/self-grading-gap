def trailing_whitespace_cleaner(text: str) -> str:
    lines = text.splitlines(keepends=True)
    cleaned_lines = [line.rstrip() for line in lines]
    return ''.join(cleaned_lines)