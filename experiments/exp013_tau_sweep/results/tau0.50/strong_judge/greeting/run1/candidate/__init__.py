def greet(names=None):
    if names is None or (isinstance(names, list) and not names):
        return "Hello, my friend."
    if isinstance(names, str):
        import re
        names = re.findall(r'"([^"]*)"|([^,]+)', names)
        names = [m[0] or m[1].strip() for m in names]
    else:
        names = [name for name in names]

    # Remove outer quotes if present
    for i in range(len(names)):
        if names[i].startswith('"') and names[i].endswith('"') and len(names[i]) >= 2:
            names[i] = names[i][1:-1]

    normal_names = [name for name in names if not name.isupper()]
    shouted_names = [name for name in names if name.isupper()]

    greeting_parts = []

    if normal_names:
        if len(normal_names) == 1:
            greeting_parts.append(f"Hello, {normal_names[0]}.")
        elif len(normal_names) == 2:
            greeting_parts.append(f"Hello, {normal_names[0]} and {normal_names[1]}.")
        else:
            greeting_parts.append(f"Hello, {', '.join(normal_names[:-1])}, and {normal_names[-1]}.\")

    if shouted_names:
        prefix = "AND " if normal_names else ""
        if len(shouted_names) == 1:
            greeting_parts.append(f"{prefix}HELLO {shouted_names[0]}!")
        else:
            greeting_parts.append(f"HELLO {' AND '.join(shouted_names)}!\")

    return ' '.join(greeting_parts)