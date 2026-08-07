from solution import spell_number

def test_spell_zero():
    # Expected: "zero"
    assert spell_number(0) == "zero"

def test_spell_single_digits():
    # Expected: "five"
    assert spell_number(5) == "five"
    # Expected: "eight"
    assert spell_number(8) == "eight"

def test_spell_ten():
    # Expected: "ten"
    assert spell_number(10) == "ten"

def test_spell_teens():
    # Expected: "thirteen"
    assert spell_number(13) == "thirteen"
    # Expected: "nineteen"
    assert spell_number(19) == "nineteen"

def test_spell_round_tens():
    # Expected: "twenty"
    assert spell_number(20) == "twenty"
    # Expected: "ninety"
    assert spell_number(90) == "ninety"

def test_spell_hyphenated_compounds():
    # Expected: "twenty-one"
    assert spell_number(21) == "twenty-one"
    # Expected: "seventy-seven"
    assert spell_number(77) == "seventy-seven"
    # Expected: "ninety-nine"
    assert spell_number(99) == "ninety-nine"

def test_spell_hundreds():
    # Expected: "one hundred"
    assert spell_number(100) == "one hundred"
    # Expected: "three hundred three"
    assert spell_number(303) == "three hundred three"
    # Expected: "five hundred fifty-five"
    assert spell_number(555) == "five hundred fifty-five"
    # Expected: "one hundred fifteen"
    assert spell_number(115) == "one hundred fifteen"

def test_spell_thousands():
    # Expected: "one thousand"
    assert spell_number(1000) == "one thousand"
    # Expected: "two thousand"
    assert spell_number(2000) == "two thousand"
    # Expected: "two thousand four hundred"
    assert spell_number(2400) == "two thousand four hundred"
    # Expected: "three thousand four hundred sixty-six"
    assert spell_number(3466) == "three thousand four hundred sixty-six"
    # Expected: "five thousand five"
    assert spell_number(5005) == "five thousand five"
    # Expected: "nine thousand nine hundred ninety-nine"
    assert spell_number(9999) == "nine thousand nine hundred ninety-nine"

def test_reject_negative_numbers():
    # Expected Error: must be in 0..9999
    with pytest.raises(ValueError, match="must be in 0..9999"):
        spell_number(-1)

def test_reject_numbers_greater_than_nine_thousand_nine_hundred_ninety_nine():
    # Expected Error: must be in 0..9999
    with pytest.raises(ValueError, match="must be in 0..9999"):
        spell_number(10000)