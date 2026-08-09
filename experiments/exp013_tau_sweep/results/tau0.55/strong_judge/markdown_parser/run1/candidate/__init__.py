def render_markdown(markdown):
    import re

    def parse_inline(text):
        # Handle bold, italic, and links
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
        return text

    def parse_line(line):
        # Check for headings
        heading_match = re.match(r'^(#+) (.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            if level > 6:
                return f'<p>{line}</p>'  # Too many hashes for heading
            return f'<h{level}>{parse_inline(heading_match.group(2))}</h{level}>'

        # Check for lists
        if line.startswith('- '):
            return f'<li>{parse_inline(line[2:])}</li>'
        return f'<p>{parse_inline(line)}</p>'

    lines = markdown.split('\n')
    blocks = []
    current_list = []

    for line in lines:
        if line.strip() == '':
            if current_list:
                blocks.append('<ul>' + ''.join(current_list) + '</ul>')
                current_list = []
        else:
            list_item = parse_line(line)
            if list_item.startswith('<li>'):
                current_list.append(list_item)
            else:
                if current_list:
                    blocks.append('<ul>' + ''.join(current_list) + '</ul>')
                    current_list = []
                blocks.append(list_item)

    if current_list:
        blocks.append('<ul>' + ''.join(current_list) + '</ul>')

    return '\n'.join(blocks).replace('<p>\n', '<p>').replace('\n</p>', '</p>')