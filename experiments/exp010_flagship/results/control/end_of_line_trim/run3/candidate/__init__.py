def trailing_whitespace_cleaner(text: str) -> str:
    return '\n'.join(line.rstrip() for line in text.splitlines(keepends=False)) + ('\n' if text.endswith('\n') else '')