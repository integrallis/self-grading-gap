def greet(names):
    if names is None or (isinstance(names, str) and not names.strip()) or (isinstance(names, list) and len(names) == 0):
        return "Hello, my friend."

    # Handle case where names is a string with commas
    if isinstance(names, str):
        names = [name.strip() for name in names.split(',')]

    # Handle quoted names
    names = [name[1:-1] if name.startswith('"') and name.endswith('"') else name for name in names]

    # Check for empty names after processing quotes
    names = [name for name in names if name]

    # Separate shouted names and normal names
    shouted_names = [name for name in names if name.isupper()]
    normal_names = [name for name in names if name.islower() or name.istitle()]

    # Prepare greetings
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
            greeting_parts.append(f"HELLO {shouted_names[0]}!")
        else:
            greeting_parts.append(f"HELLO {' AND '.join(shouted_names)}!")

    return ' '.join(greeting_parts)