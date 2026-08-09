def markdown_to_html(markdown):
    import re
    lines = markdown.split('\n')
    html = []
    list_items = []
    in_list = False

    for line in lines:
        line = line.strip()

        if not line:
            if in_list:
                html.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            continue  # skip blank lines

        # Check for headings
        heading_match = re.match(r'^(#{1,6}) (.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            html.append(f'<h{level}>{render_inline(content)}</h{level}>')
            continue

        # Check for list items
        if line.startswith('- ') and len(line) > 2:
            item = line[2:].strip()
            list_items.append(f'<li>{render_inline(item)}</li>')
            in_list = True
            continue
        else:
            if in_list:
                # Close the list if we were in one
                html.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False

        # If here, it's a plain paragraph
        html.append(f'<p>{render_inline(line)}</p>')

    # If we end in a list, close it
    if in_list:
        html.append('<ul>' + ''.join(list_items) + '</ul>')

    return '\n'.join(html)


def render_inline(text):
    import re
    # Links first to avoid affecting underscores
    text = re.sub(r'\[(.+?)\]\((.+?)\)', lambda m: f'<a href="{m.group(2)}">{render_inline(m.group(1))}</a>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    return text