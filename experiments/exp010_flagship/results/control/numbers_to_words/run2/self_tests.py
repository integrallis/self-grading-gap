from solution import spell_number

def test_spell_zero():
    assert spell_number(0) == "zero"  # AC-1.1

def test_spell_single_digits():
    assert spell_number(5) == "five"  # AC-1.1
    assert spell_number(8) == "eight"  # AC-1.1

def test_spell_ten():
    assert spell_number(10) == "ten"  # AC-1.2

def test_spell_teens():
    assert spell_number(13) == "thirteen"  # AC-1.2
    assert spell_number(19) == "nineteen"  # AC-1.2

def test_spell_round_tens():
    assert spell_number(20) == "twenty"  # AC-2.1
    assert spell_number(90) == "ninety"  # AC-2.1

def test_spell_hyphenated_tens():
    assert spell_number(21) == "twenty-one"  # AC-2.2
    assert spell_number(77) == "seventy-seven"  # AC-2.2
    assert spell_number(99) == "ninety-nine"  # AC-2.2

def test_spell_hundreds():
    assert spell_number(100) == "one hundred"  # AC-3.1
    assert spell_number(303) == "three hundred three"  # AC-3.2
    assert spell_number(555) == "five hundred fifty-five"  # AC-3.2
    assert spell_number(115) == "one hundred fifteen"  # AC-3.2

def test_spell_hundreds_no_and():
    assert spell_number(105) == "one hundred five"  # AC-3.3

def test_spell_thousands():
    assert spell_number(1000) == "one thousand"  # AC-4.1
    assert spell_number(2000) == "two thousand"  # AC-4.1
    assert spell_number(2400) == "two thousand four hundred"  # AC-4.2
    assert spell_number(3466) == "three thousand four hundred sixty-six"  # AC-4.2
    assert spell_number(5005) == "five thousand five"  # AC-4.2
    assert spell_number(9999) == "nine thousand nine hundred ninety-nine"  # AC-4.3

def test_reject_negative_numbers():
    with pytest.raises(ValueError, match="must be in 0..9999"):
        spell_number(-1)  # AC-5.1

def test_reject_numbers_greater_than_9999():
    with pytest.raises(ValueError, match="must be in 0..9999"):
        spell_number(10000)  # AC-5.2