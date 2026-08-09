def greet(names):
    import re
    if isinstance(names, str):
        # Tokenize names considering quoted entries
        tokens = re.findall(r'"([^"]*)"|([^,]+)', names)
        names = [match[0] if match[0] else match[1] for match in tokens]
        names = [name.strip() for name in names]
    if not names:
        return "Hello, my friend."

    normal_names = [name for name in names if not name.isupper()]
    shouted_names = [name for name in names if name.isupper()]

    greeting = ""
    if normal_names:
        if len(normal_names) > 2:
            greeting += "Hello, " + ", ".join(normal_names[:-1]) + ", and " + normal_names[-1] + "."
        elif len(normal_names) == 2:
            greeting += "Hello, " + " and ".join(normal_names) + "."
        else:
            greeting += "Hello, " + normal_names[0] + "."

    if shouted_names:
        shouted_greeting = "HELLO " + " AND ".join(shouted_names) + "!"
        if greeting:
            return greeting + " AND " + shouted_greeting
        return shouted_greeting

    return greeting
