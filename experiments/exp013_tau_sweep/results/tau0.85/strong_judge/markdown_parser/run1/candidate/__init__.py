def render_markdown(input_text):
    import re

    def parse_line(line):
        # Check for headings
        heading_match = re.match(r'^(#+) (.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            return f'<h{level}>{heading_match.group(2).strip()}</h{level}>'

        # Check for links
        link_pattern = r'\[(.+?)\]\((https?://[^)]+)\)'
        line = re.sub(link_pattern, r'<a href="\2">\1</a>', line)

        # Check for bold and italic
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'_(.+?)_', r'<em>\1</em>', line)

        return line.strip() if line.strip() else None

    blocks = []
    for raw_line in input_text.split('\n'):
        parsed = parse_line(raw_line)
        if parsed:
            blocks.append(parsed)
        elif blocks and blocks[-1] != '':
            blocks.append('')  # Start a new block for blank lines

    result = []
    for block in blocks:
        if block:
            if block.startswith('<h'):
                result.append(block)
            elif block.startswith('<a') or block.startswith('<strong') or block.startswith('<em'):
                result.append(f'<p>{block}</p>')
            else:
                result.append(f'<p>{block}</p>')

    return '\n'.join(result)