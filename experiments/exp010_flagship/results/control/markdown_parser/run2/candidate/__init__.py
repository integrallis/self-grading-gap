def render_markdown(text):
    lines = text.split('\n')
    result = []
    list_items = []
    in_list = False

    for line in lines:
        line = line.strip()

        if not line:
            if in_list:
                result.append('</ul>')
                in_list = False
            continue

        if line.startswith('#'):
            # Heading
            heading_level = len(line) - len(line.lstrip('#'))
            if heading_level <= 6 and line[heading_level] == ' ':
                heading_content = line[heading_level + 1:]
                # Apply inline formatting to heading content
                heading_content = heading_content.replace('**', '<strong>').replace('_', '<em>').replace('*', '<em>')
                result.append(f'<h{heading_level}>{heading_content}</h{heading_level}>')
            else:
                result.append(f'<p>{line}</p>')
                continue

        if line.startswith('- '):
            # Unordered list item
            if not in_list:
                result.append('<ul>')
                in_list = True
            list_item = line[2:]  # Skip '- '
            # Apply inline formatting to list item
            list_item = list_item.replace('**', '<strong>').replace('_', '<em>').replace('*', '<em>')
            list_items.append(f'<li>{list_item}</li>')
            continue

        if in_list:
            result.append('\n'.join(list_items))
            list_items = []
            result.append('</ul>')
            in_list = False

        # Inline formatting for paragraphs
        line = line.replace('**', '<strong>').replace('_', '<em>').replace('*', '<em>')
        result.append(f'<p>{line}</p>')

    if in_list:
        result.append('\n'.join(list_items))
        result.append('</ul>')

    return '\n'.join(result)