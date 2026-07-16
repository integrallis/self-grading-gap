def greet(names):
    if names == "" or names == []:
        return "Hello, my friend."
    if isinstance(names, str):
        names = [name.strip() for name in names.split(',')]

    regular_names = []
    shout_names = []

    for name in names:
        if isinstance(name, str) and name.isupper():
            shout_names.append(name)
        else:
            regular_names.append(name)

    greeting = "Hello"
    if regular_names:
        if len(regular_names) > 1:
            greeting += ", " + ", ".join(regular_names[:-1]) + ", and " + regular_names[-1]
        else:
            greeting += ", " + regular_names[0]
    if shout_names:
        if regular_names:
            greeting += "."
        greeting += " AND " + " AND ".join(shout_names) + "!"
    else:
        greeting += "."

    return greeting