from solution import greet

def test_greet_one_person():
    # AC-1.1: A single name is greeted as "Hello, <name>."
    assert greet("Bob") == "Hello, Bob."
    
def test_greet_no_name():
    # AC-1.2: A missing name yields "Hello, my friend."
    assert greet() == "Hello, my friend."
    assert greet([]) == "Hello, my friend."

def test_greet_single_name_in_list():
    # AC-1.3: A list containing exactly one name is greeted as that name
    assert greet(["Bob"]) == "Hello, Bob."

def test_greet_two_names():
    # AC-2.1: Two names are joined with "and"
    assert greet(["Jill", "Jane"]) == "Hello, Jill and Jane."

def test_greet_three_names():
    # AC-2.2: Three names are separated by commas with an Oxford comma
    assert greet(["Amy", "Brian", "Charlotte"]) == "Hello, Amy, Brian, and Charlotte."

def test_greet_shout_single_name():
    # AC-3.1: A name written entirely in uppercase is greeted with a shout
    assert greet("JERRY") == "HELLO JERRY!"

def test_greet_mixed_case_and_shout():
    # AC-3.3: Mixed normal and shouted names have separate greetings
    assert greet(["Amy", "BRIAN", "Charlotte"]) == "Hello, Amy and Charlotte. AND HELLO BRIAN!"

def test_greet_multiple_shouts():
    # AC-3.4: Several shouted names share a single shout
    assert greet(["BRIAN", "JERRY"]) == "HELLO BRIAN AND JERRY!"

def test_greet_comma_split():
    # AC-4.1: An entry containing a comma is split into separate names
    assert greet("Amy, Brian, Charlotte") == "Hello, Amy, Brian, and Charlotte."

def test_greet_quoted_name():
    # AC-4.2: An entry wrapped in double quotes is a single name
    assert greet('"Charlie, Dianne"') == "Hello, Charlie, Dianne."

def test_greet_lone_quote():
    # AC-4.3: A lone opening quote does not make an entry quoted
    assert greet('"Bob') == 'Hello, "Bob.'

def test_greet_empty_quotes():
    # AC-4.4: An entry consisting only of a pair of double quotes has its quotes removed
    assert greet('""') == "Hello, ."