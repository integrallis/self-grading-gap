def markdown_to_html(text):
    if not text:
        return ""

    # Split the input into lines
    lines = text.split('\n')
    html_lines = []
    current_list = []
    in_list = False

    for line in lines:
        line = line.rstrip()  # Remove trailing whitespace
        if not line:
            if in_list:
                # If in a list, finish the list if a blank line is encountered
                if current_list:
                    html_lines.append('<ul>' + ''.join(current_list) + '</ul>')
                    current_list = []
                    in_list = False
            continue

        # Check for headings
        heading_level = 0
        while heading_level < len(line) and line[heading_level] == '#':
            heading_level += 1
        if 1 <= heading_level <= 6 and line[heading_level] == ' ':
            # It's a heading
            content = line[heading_level + 1:]
            html_lines.append(f'<h{heading_level}>{handle_inline_markup(content)}</h{heading_level}>')
            continue

        # Check for list items
        if line.startswith('- '):
            list_item = handle_inline_markup(line[2:].strip())
            current_list.append(f'<li>{list_item}</li>')
            in_list = True
            continue

        # If we have a non-list, non-heading line, handle inline markup
        if in_list:
            html_lines.append('<ul>' + ''.join(current_list) + '</ul>')
            current_list = []
            in_list = False
        line = handle_inline_markup(line)
        html_lines.append(f'<p>{line}</p>')

    # Finalize any open lists
    if current_list:
        html_lines.append('<ul>' + ''.join(current_list) + '</ul>')

    return '\n'.join(html_lines)


def handle_inline_markup(text):
    # Convert **bold** to <strong>bold</strong>
    while '**' in text:
        start = text.find('**')
        end = text.find('**', start + 2)
        if end == -1:
            break
        bold_content = text[start + 2:end]
        text = text[:start] + f'<strong>{bold_content}</strong>' + text[end + 2:]

    # Convert _italic_ to <em>italic</em>
    while '_' in text:
        start = text.find('_')
        end = text.find('_', start + 1)
        if end == -1:
            break
        italic_content = text[start + 1:end]
        text = text[:start] + f'<em>{italic_content}</em>' + text[end + 1:]

    # Convert links [text](url) to <a href="url">text</a>
    while '[' in text and ']' in text and '(' in text and ')':
        start = text.find('[')
        end = text.find(']', start)
        if end == -1:
            break
        url_start = text.find('(', end)
        url_end = text.find(')', url_start)
        if url_start == -1 or url_end == -1:
            break
        link_text = text[start + 1:end]
        url = text[url_start + 1:url_end]
        text = text[:start] + f'<a href="{url}">{link_text}</a>' + text[url_end + 1:]

    return text