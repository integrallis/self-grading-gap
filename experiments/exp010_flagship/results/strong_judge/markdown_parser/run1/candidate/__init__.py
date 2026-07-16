def render_markdown(text: str) -> str:
    lines = text.split('\n')
    output = []
    list_items = []

    for line in lines:
        line = line.strip()
        if not line:
            if list_items:
                output.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
            continue

        if line.startswith('#'):
            heading_level = line.count('#')
            if heading_level <= 6 and line[heading_level] == ' ':
                content = line[heading_level + 1:]
                output.append(f'<h{heading_level}>{render_inline(content)}</h{heading_level}>')
            else:
                output.append(f'<p>{line}</p>')
        elif line.startswith('- '):
            list_items.append(f'<li>{render_inline(line[2:])}</li>')
        else:
            if list_items:
                output.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
            output.append(f'<p>{render_inline(line)}</p>')

    if list_items:
        output.append('<ul>' + ''.join(list_items) + '</ul>')

    return '\n'.join(output)


def render_inline(text: str) -> str:
    output = []
    i = 0
    while i < len(text):
        if text[i:i+2] == '**':
            end = text.find('**', i + 2)
            if end != -1:
                output.append('<strong>' + render_inline(text[i + 2:end]) + '</strong>')
                i = end + 2
                continue
        elif text[i] == '_':
            end = text.find('_', i + 1)
            if end != -1:
                output.append('<em>' + text[i + 1:end] + '</em>')
                i = end + 1
                continue
        elif text[i] == '[':
            end_label = text.find(']', i)
            end_url = text.find(')', end_label)
            if end_label != -1 and end_url != -1:
                label = text[i + 1:end_label]
                url = text[end_label + 2:end_url]
                output.append(f'<a href="{url}">{render_inline(label)}</a>')
                i = end_url + 1
                continue
        output.append(text[i])
        i += 1
    return ''.join(output)