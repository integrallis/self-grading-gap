def greet(names):
    if names is None or (isinstance(names, list) and not names):
        return "Hello, my friend."

    # Handle input as a list of names
    if isinstance(names, str):
        names = [name.strip() for name in names.split(",")]
    else:
        names = [name.strip() for sublist in names for name in sublist.split(",")]

    # Clean up names by stripping whitespace and removing outer quotes
    cleaned_names = []
    for name in names:
        name = name.strip()
        if name.startswith('"') and name.endswith('"'):
            name = name[1:-1]
        cleaned_names.append(name)

    normal_names = [name for name in cleaned_names if not name.isupper()]
    shouted_names = [name for name in cleaned_names if name.isupper()]

    # Generate normal greeting
    if normal_names:
        if len(normal_names) == 1:
            normal_greeting = f"Hello, {normal_names[0]}."
        elif len(normal_names) == 2:
            normal_greeting = f"Hello, {normal_names[0]} and {normal_names[1]}."
        else:
            normal_greeting = f"Hello, {', '.join(normal_names[:-1])}, and {normal_names[-1]}."
    else:
        normal_greeting = ""

    # Generate shout greeting
    if shouted_names:
        if len(shouted_names) == 1:
            shout_greeting = f"HELLO {shouted_names[0]}!"
        else:
            shout_greeting = f"HELLO {' AND '.join(shouted_names)}!"
    else:
        shout_greeting = ""

    # Combine greetings
    if normal_greeting and shout_greeting:
        return normal_greeting + " AND " + shout_greeting
    return normal_greeting or shout_greeting