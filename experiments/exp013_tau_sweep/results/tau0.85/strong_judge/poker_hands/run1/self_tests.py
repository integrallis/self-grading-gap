from solution import read_hand, categorize_hand, showdown

def test_read_hand_valid():
    assert read_hand("2H 3D 5S 9C KD") == ["2H", "3D", "5S", "9C", "KD"]
    assert read_hand("10H JD QS KH AC") == ["10H", "JD", "QS", "KH", "AC"]
    assert read_hand("TH JH QH KH AH") == ["10H", "JH", "QH", "KH", "AH"]  # Testing "T" notation

def test_read_hand_invalid_card():
    assert read_hand("1Z 3D 5S 9C KD") == "invalid card: '1Z'"
    assert read_hand("1H 3D 5S 9C KD") == "invalid card: '1H'"  # Testing unknown value with valid suit
    assert read_hand("2H 3D 5S 9C 10X") == "invalid card: '10X'"

def test_read_hand_invalid_length():
    assert read_hand("2H 3D 5S") == "a hand must contain exactly 5 cards"
    assert read_hand("2H 3D 5S 9C KD 6H") == "a hand must contain exactly 5 cards"

def test_categorize_hand_high_card():
    assert categorize_hand("2H 3D 5S 9C KD") == "high card"
    assert categorize_hand("AH 2D 3S 4C 5H") == "high card"  # Testing high card

def test_categorize_hand_pair():
    assert categorize_hand("2H 2D 5S 9C KD") == "pair"
    assert categorize_hand("10H 10D 5S 9C KD") == "pair"

def test_categorize_hand_two_pairs():
    assert categorize_hand("2H 2D 5S 5C KD") == "two pairs"
    assert categorize_hand("10H 10D 5S 5C KD") == "two pairs"

def test_categorize_hand_three_of_a_kind():
    assert categorize_hand("2H 2D 2S 5C KD") == "three of a kind"
    assert categorize_hand("10H 10D 10S 5C KD") == "three of a kind"

def test_categorize_hand_straight():
    assert categorize_hand("2H 3D 4S 5C 6H") == "straight"  # Valid straight
    assert categorize_hand("AH 2D 3S 4C 5H") == "high card"  # A-2-3-4-5 is not a straight

def test_categorize_hand_flush():
    assert categorize_hand("2H 5H 9H KH AH") == "flush"
    assert categorize_hand("3D 5D 9D KD AD") == "flush"

def test_categorize_hand_full_house():
    assert categorize_hand("2H 2D 2S 5C 5D") == "full house"
    assert categorize_hand("10H 10D 10S 5C 5D") == "full house"

def test_categorize_hand_four_of_a_kind():
    assert categorize_hand("2H 2D 2S 2C 5D") == "four of a kind"
    assert categorize_hand("10H 10D 10S 10C 5D") == "four of a kind"

def test_categorize_hand_straight_flush():
    assert categorize_hand("2H 3H 4H 5H 6H") == "straight flush"
    assert categorize_hand("10H JH QH KH AH") == "straight flush"  # Valid straight flush

def test_showdown_black_wins():
    assert showdown("2H 3D 5S 9C KD", "2H 2D 5S 9C KD") == "White wins. - with pair"  # Black has high card, White has pair

def test_showdown_white_wins():
    assert showdown("2H 3D 5S 9C KD", "10H JD QS KH AC") == "White wins. - with straight"  # White has a straight

def test_showdown_tie():
    assert showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C KD") == "Tie."  # Identical hands

def test_showdown_black_wins_high_card():
    assert showdown("KH 3D 5S 9C 4D", "10H 3D 5S 9C 2D") == "Black wins. - with high card: King"  # Black has higher card

def test_showdown_black_wins_pair():
    assert showdown("8H 8D 5S 6C KD", "8D 3D 5S 6H KD") == "Black wins. - with pair: 8"  # Black's pair beats White's pair

def test_showdown_black_wins_pair_kicker():
    assert showdown("8H 8D 5S 6C KD", "8D 8C 5S 6H 2D") == "Black wins. - with pair: King"  # Black's kicker beats White's kicker

def test_showdown_black_wins_two_pairs():
    assert showdown("8H 8D 5S 5C KD", "8D 8S 5D 5H 2C") == "Black wins. - with two pairs: King"  # Higher kicker wins

def test_showdown_deciding_value_straight():
    assert showdown("2H 3D 4S 5C 6H", "3H 4D 5S 6C 7H") == "White wins. - with straight: 7"

def test_showdown_deciding_value_flush():
    assert showdown("2H 5H 9H KH AH", "3D 5D 9D KD AD") == "White wins. - with flush: 3"  # White's 3 beats Black's 2

def test_showdown_deciding_value_four_of_a_kind():
    assert showdown("8H 8D 8S 8C 5D", "2H 2D 2S 2C 10D") == "Black wins. - with four of a kind: 8"  # Black's four 8s beat White's four 2s

def test_showdown_deciding_value_full_house():
    assert showdown("2H 2D 2S 5C 5D", "10H 10D 10S 5C 5D") == "Black wins. - with full house: 2"  # Black's full house beats White's

def test_showdown_deciding_value_three_of_a_kind():
    assert showdown("2H 2D 2S 5C 8D", "10H 10D 10S 5C 5D") == "White wins. - with three of a kind: 10"  # White's three of a kind beats Black's

def test_showdown_deciding_value_straight_flush():
    assert showdown("2H 3H 4H 5H 6H", "3H 4H 5H 6H 7H") == "White wins. - with straight flush: 7"  # Higher straight flush wins