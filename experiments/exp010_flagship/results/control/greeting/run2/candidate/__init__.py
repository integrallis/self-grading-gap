def greet(names):
    if isinstance(names, str):
        names = [names]
    elif names == "" or not names:
        return "Hello, my friend."
    else:
        # Handle quoted names
        if isinstance(names, str) and names.startswith('"') and names.endswith('"'):
            names = [names[1:-1]]
        names = [name.strip() for name in names]

    normal_names = [name for name in names if not name.isupper()]
    shouted_names = [name for name in names if name.isupper()]

    if not normal_names and shouted_names:
        return "HELLO " + " AND ".join(shouted_names) + "!"

    greetings = []
    if normal_names:
        if len(normal_names) == 1:
            greetings.append(f"Hello, {normal_names[0]}.")
        elif len(normal_names) == 2:
            greetings.append(f"Hello, {normal_names[0]} and {normal_names[1]}.")
        else:
            greetings.append(f"Hello, {', '.join(normal_names[:-1])}, and {normal_names[-1]}.")

    if shouted_names:
        if len(shouted_names) == 1:
            greetings.append(f"AND HELLO {shouted_names[0]}!")
        else:
            greetings.append("HELLO " + " AND ".join(shouted_names) + "!")

    return " ".join(greetings)