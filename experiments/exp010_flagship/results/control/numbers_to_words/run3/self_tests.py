# test_solution.py

from solution import number_to_words

def test_zero():
    assert number_to_words(0) == "zero"  # Specification AC-1.1

def test_single_digits():
    assert number_to_words(5) == "five"  # Specification AC-1.1
    assert number_to_words(8) == "eight"  # Specification AC-1.1

def test_ten():
    assert number_to_words(10) == "ten"  # Specification AC-1.2

def test_teen_numbers():
    assert number_to_words(13) == "thirteen"  # Specification AC-1.2
    assert number_to_words(19) == "nineteen"  # Specification AC-1.2

def test_round_tens():
    assert number_to_words(20) == "twenty"  # Specification AC-2.1
    assert number_to_words(90) == "ninety"  # Specification AC-2.1

def test_hyphenated_tens_units():
    assert number_to_words(21) == "twenty-one"  # Specification AC-2.2
    assert number_to_words(77) == "seventy-seven"  # Specification AC-2.2
    assert number_to_words(99) == "ninety-nine"  # Specification AC-2.2

def test_hundreds():
    assert number_to_words(100) == "one hundred"  # Specification AC-3.1
    assert number_to_words(303) == "three hundred three"  # Specification AC-3.2
    assert number_to_words(555) == "five hundred fifty-five"  # Specification AC-3.2
    assert number_to_words(115) == "one hundred fifteen"  # Specification AC-3.2

def test_hundreds_no_and():
    assert number_to_words(100) == "one hundred"  # Specification AC-3.1
    assert number_to_words(200) == "two hundred"  # Specification AC-3.1
    assert number_to_words(305) == "three hundred five"  # Specification AC-3.2

def test_thousands():
    assert number_to_words(1000) == "one thousand"  # Specification AC-4.1
    assert number_to_words(2000) == "two thousand"  # Specification AC-4.1
    assert number_to_words(2400) == "two thousand four hundred"  # Specification AC-4.2
    assert number_to_words(3466) == "three thousand four hundred sixty-six"  # Specification AC-4.2
    assert number_to_words(5005) == "five thousand five"  # Specification AC-4.2
    assert number_to_words(9999) == "nine thousand nine hundred ninety-nine"  # Specification AC-4.3

def test_reject_negative_numbers():
    with pytest.raises(ValueError, match="must be in 0..9999"):
        number_to_words(-1)  # Specification AC-5.1

def test_reject_numbers_greater_than_9999():
    with pytest.raises(ValueError, match="must be in 0..9999"):
        number_to_words(10000)  # Specification AC-5.2