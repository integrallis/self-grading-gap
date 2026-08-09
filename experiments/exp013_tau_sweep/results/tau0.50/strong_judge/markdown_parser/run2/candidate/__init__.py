import re

def render_markdown(text):
    # Split the input into lines
    lines = text.split('\n')
    # Result list to store blocks
    result = []
    current_list = []

    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:
            if current_list:
                result.append('<ul>' + ''.join(current_list) + '</ul>')
                current_list = []
            continue  # Ignore blank lines

        # Heading detection
        heading_match = re.match(r'^(#{1,6}) (.+)$', stripped_line)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            result.append(f'<h{level}>{render_inline(content)}</h{level}>')
            continue

        # List item detection
        if stripped_line.startswith('- '):
            list_item = f'<li>{render_inline(stripped_line[2:])}</li>'
            current_list.append(list_item)
            continue

        # If we reach here, it’s plain text
        if current_list:
            result.append('<ul>' + ''.join(current_list) + '</ul>')
            current_list = []
        result.append(f'<p>{render_inline(stripped_line)}</p>')

    # Handle any remaining list items
    if current_list:
        result.append('<ul>' + ''.join(current_list) + '</ul>')

    return '\n'.join(result)


def render_inline(text):
    # Render bold, italic, and links inline
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text