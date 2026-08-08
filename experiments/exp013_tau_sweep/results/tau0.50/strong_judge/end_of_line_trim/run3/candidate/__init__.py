'''The solution package.'''

__version__ = "0.1.0"

def trailing_whitespace_cleaner(text: str) -> str:
    lines = text.splitlines(keepends=True)
    cleaned_lines = [line.rstrip() for line in lines]
    if cleaned_lines and cleaned_lines[-1].endswith(('\n', '\r')):
        cleaned_lines[-1] = cleaned_lines[-1].rstrip(' \t')
    return ''.join(cleaned_lines)