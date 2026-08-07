def greet(names):
    if names is None or (isinstance(names, list) and not names):
        return "Hello, my friend."

    if isinstance(names, str):
        names = parse_names(names)
    elif not isinstance(names, list):
        names = [names]

    normal_names = []
    shouted_names = []

    for name in names:
        if name.isupper():
            shouted_names.append(name)
        else:
            normal_names.append(name)

    normal_phrase = format_normal_names(normal_names)

    if shouted_names:
        shout_greeting = " AND ".join(shouted_names)
        if normal_names:
            greeting = f"Hello, {normal_phrase}. AND HELLO {shout_greeting}!"
        else:
            greeting = f"HELLO {shout_greeting}!"
    else:
        greeting = f"Hello, {normal_phrase}."

    return greeting.strip()


def parse_names(name_string):
    names = []
    current_name = []
    in_quotes = False

    for char in name_string:
        if char == '"':
            in_quotes = not in_quotes
            if not in_quotes:
                current_name.append(char)
        elif char == ',' and not in_quotes:
            if current_name:
                names.append(''.join(current_name).strip())
                current_name = []
        else:
            current_name.append(char)

    if current_name:
        entry = ''.join(current_name).strip()
        if entry.startswith('"') and entry.endswith('"'):
            names.append(entry[1:-1])
        else:
            names.append(entry)

    return names


def format_normal_names(names):
    if len(names) == 0:
        return ''
    elif len(names) == 1:
        return names[0]
    elif len(names) == 2:
        return f"{names[0]} and {names[1]}"
    else:
        return f"{', '.join(names[:-1])}, and {names[-1]}"