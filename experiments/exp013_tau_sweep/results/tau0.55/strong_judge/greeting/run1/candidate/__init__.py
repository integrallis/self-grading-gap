def polite_greeter(names=None):
    if names is None:
        names = []
    elif isinstance(names, str):
        names = [name.strip() for name in parse_names(names)]

    normal_names = []
    shouted_names = []

    for name in names:
        if name.isupper():
            shouted_names.append(name)
        else:
            normal_names.append(name.strip())

    greeting_parts = []

    if normal_names:
        if len(normal_names) == 1:
            greeting_parts.append(f"Hello, {normal_names[0]}.")
        elif len(normal_names) == 2:
            greeting_parts.append(f"Hello, {normal_names[0]} and {normal_names[1]}.")
        else:
            greeting_parts.append(f"Hello, {', '.join(normal_names[:-1])}, and {normal_names[-1]}.")

    if shouted_names:
        if len(shouted_names) == 1:
            if not normal_names:
                greeting_parts.append(f"HELLO {shouted_names[0]}!")
            else:
                greeting_parts.append(f"AND HELLO {shouted_names[0]}!")
        else:
            greeting_parts.append(f"HELLO {' AND '.join(shouted_names)}!")

    if not greeting_parts:
        return "Hello, my friend."

    return ' '.join(greeting_parts)


def parse_names(names):
    import re
    # Matches quoted strings or unquoted names separated by commas
    pattern = r'"([^"]*)"|([^,]+)'
    return [match[0] or match[1] for match in re.findall(pattern, names)]
