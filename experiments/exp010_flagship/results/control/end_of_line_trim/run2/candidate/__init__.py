def trailing_whitespace_cleaner(text):
    stripped_text = text.rstrip(' 	')
    if text.endswith('\n'):
        return stripped_text + '\n'
    return stripped_text