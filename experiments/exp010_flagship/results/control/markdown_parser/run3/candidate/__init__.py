def markdown_to_html(markdown):
    import re

    def convert_line(line):
        # Check for headings
        heading_match = re.match(r'^(#{1,6}) (.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', heading_match.group(2).strip())
            line = re.sub(r'_([^_]+)_', r'<em>\1</em>', line)
            return f'<h{level}>{line}</h{level}>'

        # Check for unordered list items
        if line.startswith('- '):
            return f'<li>{re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', re.sub(r'_([^_]+)_', r'<em>\1</em>', line[2:].strip()))}</li>'

        # Check for links
        line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)

        # Check for bold and italic text
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'_([^_]+)_', r'<em>\1</em>', line)

        return f'<p>{line.strip()}</p>'

    # Split the input into lines and process each line
    lines = markdown.split('\n')
    result = []
    current_list = []

    for line in lines:
        if line.strip() == '':
            if current_list:
                result.append('<ul>' + ''.join(current_list) + '</ul>')
                current_list = []
            continue
        if line.startswith('- '):
            current_list.append(convert_line(line))
        else:
            if current_list:
                result.append('<ul>' + ''.join(current_list) + '</ul>')
                current_list = []
            result.append(convert_line(line))

    if current_list:
        result.append('<ul>' + ''.join(current_list) + '</ul>')

    return '\n'.join(result)