import re

def render_markdown(text):
    lines = text.split('\n')
    result = []
    current_list = []

    def close_current_list():
        if current_list:
            result.append('<ul>' + ''.join(current_list) + '</ul>')
            current_list.clear()

    for line in lines:
        line = line.rstrip()  # Strip trailing spaces
        if not line:
            close_current_list()
            continue
        # Check for headings
        heading_match = re.match(r'^(#{1,6}) (.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            content = render_inline(heading_match.group(2))
            close_current_list()
            result.append(f'<h{level}>{content}</h{level}>')
            continue
        # Check for list items
        list_match = re.match(r'^- (.+)$', line)
        if list_match:
            current_list.append(f'<li>{render_inline(list_match.group(1))}</li>')
            continue
        # Regular paragraph
        close_current_list()
        result.append(f'<p>{render_inline(line)}</p>')

    close_current_list()  # Close any open list at the end
    return '\n'.join(result)


def render_inline(text):
    # Render bold and italic first
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    # Render links afterwards
    def replace_link(match):
        return f'<a href="{match.group(2)}">{render_inline(match.group(1))}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, text)
    return text