from solution import greet

def test_greet_one_person():
    # AC-1.1: A single name is greeted as "Hello, <name>."
    assert greet("Bob") == "Hello, Bob."  # Expected: "Hello, Bob."

def test_greet_no_person():
    # AC-1.2: A missing name, or an empty list of names, yields "Hello, my friend."
    assert greet([]) == "Hello, my friend."  # Expected: "Hello, my friend."

def test_greet_one_person_in_list():
    # AC-1.3: A list containing exactly one name is greeted the same way as that single name on its own.
    assert greet(["Bob"]) == "Hello, Bob."  # Expected: "Hello, Bob."

def test_greet_two_people():
    # AC-2.1: Two names are joined with "and"
    assert greet(["Jill", "Jane"]) == "Hello, Jill and Jane."  # Expected: "Hello, Jill and Jane."

def test_greet_three_or_more_people():
    # AC-2.2: Three or more names are separated by commas with an Oxford comma before the final "and".
    assert greet(["Amy", "Brian", "Charlotte"]) == "Hello, Amy, Brian, and Charlotte."  # Expected: "Hello, Amy, Brian, and Charlotte."
    assert greet(["Amy", "Brian", "Charlotte", "Dora"]) == "Hello, Amy, Brian, Charlotte, and Dora."  # Expected: "Hello, Amy, Brian, Charlotte, and Dora."

def test_greet_uppercase_name():
    # AC-3.1: A name written entirely in uppercase is a shout and is answered with a shouted greeting.
    assert greet("JERRY") == "HELLO JERRY!"  # Expected: "HELLO JERRY!"

def test_greet_mixed_names():
    # AC-3.3: When normal and shouted names are mixed, the normal greeting comes first.
    assert greet(["Amy", "BRIAN", "Charlotte"]) == "Hello, Amy and Charlotte. AND HELLO BRIAN!"  # Expected: "Hello, Amy and Charlotte. AND HELLO BRIAN!"

def test_greet_multiple_shouted_names():
    # AC-3.4: Several shouted names share a single shout, joined by "AND".
    assert greet(["BRIAN", "JERRY"]) == "HELLO BRIAN AND JERRY!"  # Expected: "HELLO BRIAN AND JERRY!"

def test_greet_names_with_commas():
    # AC-4.1: An entry containing a comma is split into separate names.
    assert greet("Charlie, Dianne") == "Hello, Charlie and Dianne."  # Expected: "Hello, Charlie and Dianne."
    assert greet(" Charlie , Dianne ") == "Hello, Charlie and Dianne."  # Expected: "Hello, Charlie and Dianne."

def test_greet_names_with_quotes():
    # AC-4.2: An entry wrapped in double quotes is a single name.
    assert greet('"Charlie, Dianne"') == "Hello, Charlie, Dianne."  # Expected: "Hello, Charlie, Dianne."

def test_greet_lone_quote():
    # AC-4.3: A lone opening quote does not make an entry quoted.
    assert greet('"Bob') == "Hello, \"Bob."  # Expected: "Hello, "Bob."

def test_greet_empty_quotes():
    # AC-4.4: An entry consisting only of a pair of double quotes has its quotes removed, leaving an empty name.
    assert greet('""') == "Hello, ."  # Expected: "Hello, ."

def test_greet_lowercase_name():
    # Test for a lowercase name
    assert greet("bob") == "Hello, bob."  # Expected: "Hello, bob."