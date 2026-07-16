def markdown_to_html(text):
    import re

    def parse_block(block):
        # Check for links first to avoid underscores in URLs being misinterpreted
        link_match = re.match(r'\[(.+?)\]\((.+?)\)', block)
        if link_match:
            link_text, url = link_match.groups()
            return f'<p><a href="{url}">{link_text}</a></p>'

        # Process inline emphasis after links
        block = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', block)
        block = re.sub(r'_(.+?)_', r'<em>\1</em>', block)

        # Check for headings
        match = re.match(r'^(#{1,6}) (.+)$', block)
        if match:
            level, content = match.groups()
            heading_level = len(level)
            return f'<h{heading_level}>{content}</h{heading_level}>'

        # Check for list items
        if block.startswith('- '):
            return f'<li>{block[2:]}</li>'

        # If nothing else matches, return as a paragraph
        return f'<p>{block}</p>'

    blocks = text.split('\n')
    output = []
    current_list = []

    for block in blocks:
        parsed_block = parse_block(block)
        if parsed_block.strip() == '':
            if current_list:
                output.append('<ul>' + ''.join(current_list) + '</ul>')
                current_list = []
            continue
        if parsed_block.startswith('<li>'):
            current_list.append(parsed_block)
        else:
            if current_list:
                output.append('<ul>' + ''.join(current_list) + '</ul>')
                current_list = []
            output.append(parsed_block)

    if current_list:
        output.append('<ul>' + ''.join(current_list) + '</ul>')
    return '\n'.join(output)