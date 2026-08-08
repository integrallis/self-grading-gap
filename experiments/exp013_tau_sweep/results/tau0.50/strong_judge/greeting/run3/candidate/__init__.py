def greet(names):
    if names is None or (isinstance(names, list) and not names):
        return "Hello, my friend."
    elif isinstance(names, str):
        names = parse_names(names)
    else:
        names = list(map(str, names))

    normal_names = [name for name in names if not name.isupper()]
    shouted_names = [name for name in names if name.isupper()]

    greeting_parts = []

    if normal_names:
        if len(normal_names) == 1:
            greeting_parts.append(f"Hello, {normal_names[0]}.")
        elif len(normal_names) == 2:
            greeting_parts.append(f"Hello, {normal_names[0]} and {normal_names[1]}.")
        else:
            greeting_parts.append(f"Hello, {', '.join(normal_names[:-1])}, and {normal_names[-1]}.")

    if shouted_names:
        prefix = "AND " if normal_names else ""
        if len(shouted_names) == 1:
            greeting_parts.append(f"{prefix}HELLO {shouted_names[0]}!")
        else:
            greeting_parts.append(f"HELLO {' AND '.join(shouted_names)}!")

    return ' '.join(greeting_parts)


def parse_names(input_string):
    import re
    # Match quoted names and separate by commas not inside quotes
    pattern = r'"(.*?)"|([^,]+)'
    matches = re.findall(pattern, input_string)
    names = [m[0] if m[0] else m[1] for m in matches]
    # Strip spaces and handle empty quotes
    return [name.strip() if name.strip() != '"' else '' for name in names]
