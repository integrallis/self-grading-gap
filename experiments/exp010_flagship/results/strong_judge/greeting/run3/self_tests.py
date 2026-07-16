# your complete test file
def test_greet_single_name():
    # AC-1.1: A single name is greeted as "Hello, <name>."
    assert greet("Bob") == "Hello, Bob."

def test_greet_no_name_empty_list():
    # AC-1.2: An empty list of names yields "Hello, my friend."
    assert greet([]) == "Hello, my friend."

def test_greet_no_name_none():
    # AC-1.2: A missing name yields "Hello, my friend."
    assert greet(None) == "Hello, my friend."

def test_greet_one_name_in_list():
    # AC-1.3: A list containing exactly one name is greeted the same way as that single name on its own.
    assert greet(["Bob"]) == "Hello, Bob."

def test_greet_two_names():
    # AC-2.1: Two names are joined with "and".
    assert greet(["Jill", "Jane"]) == "Hello, Jill and Jane."

def test_greet_three_names():
    # AC-2.2: Three or more names are separated by commas with an Oxford comma before the final "and".
    assert greet(["Amy", "Brian", "Charlotte"]) == "Hello, Amy, Brian, and Charlotte."

def test_greet_four_names():
    # Additional test for four names with Oxford comma.
    assert greet(["Amy", "Brian", "Charlotte", "David"]) == "Hello, Amy, Brian, Charlotte, and David."

def test_greet_shouted_name():
    # AC-3.1: A name written entirely in uppercase is a shout and is answered with a shouted greeting.
    assert greet("JERRY") == "HELLO JERRY!"

def test_greet_lowercase_name():
    # AC-3.2: Lowercase and mixed-case names are not shouts and receive the normal greeting.
    assert greet("alice") == "Hello, alice."

def test_greet_mixed_case_names():
    # AC-3.2: Lowercase and mixed-case names are not shouts and receive the normal greeting.
    assert greet("Alice") == "Hello, Alice."

def test_greet_mixed_names():
    # AC-3.3: When normal and shouted names are mixed, the normal greeting comes first, followed by a separate shouted greeting.
    assert greet(["Amy", "BRIAN", "Charlotte"]) == "Hello, Amy and Charlotte. AND HELLO BRIAN!"

def test_greet_multiple_shouted_names():
    # AC-3.4: Several shouted names share a single shout, joined by "AND".
    assert greet(["BRIAN", "JERRY"]) == "HELLO BRIAN AND JERRY!"

def test_greet_entry_with_comma():
    # AC-4.1: An entry containing a comma is split into separate names.
    assert greet("Charlie, Dianne") == "Hello, Charlie and Dianne."

def test_greet_entry_with_quotes():
    # AC-4.2: An entry wrapped in double quotes is a single name.
    assert greet('"Charlie, Dianne"') == "Hello, Charlie, Dianne."

def test_greet_lone_quote():
    # AC-4.3: A lone opening quote does not make an entry quoted.
    assert greet('"Bob') == 'Hello, "Bob.'

def test_greet_empty_quotes():
    # AC-4.4: An entry consisting only of a pair of double quotes has its quotes removed.
    assert greet('""') == "Hello, ."

def test_greet_entry_with_whitespace():
    # Additional test for whitespace around split components.
    assert greet(" Amy , Brian , Charlotte ") == "Hello, Amy, Brian, and Charlotte."