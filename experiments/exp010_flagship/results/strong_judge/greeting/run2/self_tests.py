from solution import greet

def test_greet_single_name():
    # "Hello, Bob."
    assert greet("Bob") == "Hello, Bob."

def test_greet_no_name():
    # "Hello, my friend."
    assert greet(None) == "Hello, my friend."

def test_greet_empty_list():
    # "Hello, my friend."
    assert greet([]) == "Hello, my friend."

def test_greet_one_name_in_list():
    # "Hello, Bob."
    assert greet(["Bob"]) == "Hello, Bob."

def test_greet_two_names():
    # "Hello, Jill and Jane."
    assert greet(["Jill", "Jane"]) == "Hello, Jill and Jane."

def test_greet_three_names():
    # "Hello, Amy, Brian, and Charlotte."
    assert greet(["Amy", "Brian", "Charlotte"]) == "Hello, Amy, Brian, and Charlotte."

def test_greet_four_names():
    # "Hello, Amy, Brian, Charlotte, and David."
    assert greet(["Amy", "Brian", "Charlotte", "David"]) == "Hello, Amy, Brian, Charlotte, and David."

def test_greet_shouted_name():
    # "HELLO JERRY!"
    assert greet("JERRY") == "HELLO JERRY!"

def test_greet_lowercase_name():
    # "Hello, bob."
    assert greet("bob") == "Hello, bob."

def test_greet_mixed_case_and_shouted_names():
    # "Hello, Amy and Charlotte. AND HELLO BRIAN!"
    assert greet(["Amy", "Charlotte", "BRIAN"]) == "Hello, Amy and Charlotte. AND HELLO BRIAN!"

def test_greet_multiple_shouted_names():
    # "HELLO BRIAN AND JERRY!"
    assert greet(["BRIAN", "JERRY"]) == "HELLO BRIAN AND JERRY!"

def test_greet_comma_split():
    # "Hello, Charlie and Dianne."
    assert greet("Charlie, Dianne") == "Hello, Charlie and Dianne."
    # Testing with spaces around comma
    assert greet([" Charlie , Dianne "]) == "Hello, Charlie and Dianne."

def test_greet_quoted_name():
    # "Hello, Charlie, Dianne."
    assert greet('"Charlie, Dianne"') == "Hello, Charlie, Dianne."

def test_greet_lone_quote():
    # "Hello, "Bob."
    assert greet('"Bob') == "Hello, \"Bob."

def test_greet_empty_quotes():
    # "Hello, ."
    assert greet('""') == "Hello, ."

def test_greet_combined_cases():
    # "Hello, Amy and Charlotte. AND HELLO BRIAN!"
    assert greet(['Amy', 'BRIAN', 'Charlotte']) == "Hello, Amy and Charlotte. AND HELLO BRIAN!"