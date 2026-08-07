from solution import polite_greeter

def test_greet_one_person():
    # AC-1.1: A single name is greeted as "Hello, <name>."
    assert polite_greeter("Bob") == "Hello, Bob."  # Hello, Bob.
    
def test_greet_nobody():
    # AC-1.2: A missing name, or an empty list of names, yields "Hello, my friend."
    assert polite_greeter() == "Hello, my friend."  # Hello, my friend.
    assert polite_greeter([]) == "Hello, my friend."  # Hello, my friend.

def test_greet_single_name_in_list():
    # AC-1.3: A list containing exactly one name is greeted the same way as that single name on its own.
    assert polite_greeter(["Bob"]) == "Hello, Bob."  # Hello, Bob.

def test_greet_two_names():
    # AC-2.1: Two names are joined with "and".
    assert polite_greeter(["Jill", "Jane"]) == "Hello, Jill and Jane."  # Hello, Jill and Jane.

def test_greet_three_or_more_names():
    # AC-2.2: Three or more names are separated by commas with an Oxford comma before the final "and".
    assert polite_greeter(["Amy", "Brian", "Charlotte"]) == "Hello, Amy, Brian, and Charlotte."  # Hello, Amy, Brian, and Charlotte.
    assert polite_greeter(["Amy", "Brian", "Charlotte", "Diana"]) == "Hello, Amy, Brian, Charlotte, and Diana."  # Hello, Amy, Brian, Charlotte, and Diana.

def test_greet_shouted_name():
    # AC-3.1: A name written entirely in uppercase is a shout and is answered with a shouted greeting.
    assert polite_greeter("JERRY") == "HELLO JERRY!"  # HELLO JERRY!

def test_greet_lowercase_name():
    # AC-3.2: Lowercase names are not shouts and receive the normal greeting.
    assert polite_greeter("bob") == "Hello, bob."  # Hello, bob.

def test_greet_mixed_case_name():
    # AC-3.2: Mixed-case names are not shouts and receive the normal greeting.
    assert polite_greeter("BoB") == "Hello, BoB."  # Hello, BoB.

def test_greet_mixed_case_and_shouted_names():
    # AC-3.3: When normal and shouted names are mixed, the normal greeting comes first, followed by a separate shouted greeting.
    assert polite_greeter(["Amy", "BRIAN", "Charlotte"]) == "Hello, Amy and Charlotte. AND HELLO BRIAN!"  # Hello, Amy and Charlotte. AND HELLO BRIAN!

def test_greet_multiple_shouted_names():
    # AC-3.4: Several shouted names share a single shout, joined by "AND".
    assert polite_greeter(["BRIAN", "JERRY"]) == "HELLO BRIAN AND JERRY!"  # HELLO BRIAN AND JERRY!

def test_greet_names_with_commas():
    # AC-4.1: An entry containing a comma is split into separate names.
    assert polite_greeter("Alice, Bob") == "Hello, Alice and Bob."  # Hello, Alice and Bob.

def test_greet_quoted_names_with_commas():
    # AC-4.2: An entry wrapped in double quotes is a single name.
    assert polite_greeter('"Charlie, Dianne"') == "Hello, Charlie, Dianne."  # Hello, Charlie, Dianne.

def test_greet_lone_quote():
    # AC-4.3: A lone opening quote does not make an entry quoted.
    assert polite_greeter('"Bob') == 'Hello, "Bob.'  # Hello, "Bob.

def test_greet_empty_quotes():
    # AC-4.4: An entry consisting only of a pair of double quotes has its quotes removed, leaving an empty name.
    assert polite_greeter('""') == "Hello, ."  # Hello, .

def test_greet_names_with_trailing_whitespace():
    # AC-4.1: An entry containing a comma is split into separate names, trimming trailing whitespace.
    assert polite_greeter(" Alice , Bob  ") == "Hello, Alice and Bob."  # Hello, Alice and Bob.