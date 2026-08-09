from solution import showdown

def test_read_hand_invalid_card_count():
    assert showdown("2H 3D 5S 9C", "2H 3D 5S 9C KD") == "a hand must contain exactly 5 cards"
    assert showdown("2H 3D 5S 9C KD 6S", "2H 3D 5S 9C KD") == "a hand must contain exactly 5 cards"

def test_read_hand_invalid_card_value():
    assert showdown("1H 3D 5S 9C KD", "2H 3D 5S 9C KD") == "invalid card: '1H'"
    assert showdown("2H 3D 5S 9C KZ", "2H 3D 5S 9C KD") == "invalid card: 'KZ'"

def test_read_hand_invalid_card_suit():
    assert showdown("2H 3D 5S 9C KZ", "2H 3D 5S 9C KD") == "invalid card: 'KZ'"
    assert showdown("2H 3D 5S 9C 10X", "2H 3D 5S 9C KD") == "invalid card: '10X'"

def test_read_hand_valid_with_ten():
    assert showdown("10H JH QH KH AH", "2H 3D 5S 9C KD") != "invalid card: '10H'"

def test_name_hand_category_high_card():
    assert showdown("2H 3D 5S 9C KD", "6H 7D 8S 9C 10D") == "White wins. - with high card: 10"  # White has 10 high
    assert showdown("TH JH QH KH AH", "2H 3D 5S 9C KD") == "Black wins. - with straight flush"  # Black has a straight flush

def test_name_hand_category_pair():
    assert showdown("2H 2D 5S 9C KD", "3H 3D 5S 9C KD") == "White wins. - with pair: 3"  # White has pair of 3s
    assert showdown("5H 5D 5S 9C KD", "3H 3D 5S 9C KD") == "Black wins. - with three of a kind"  # Black has three of a kind

def test_name_hand_category_two_pairs():
    assert showdown("2H 2D 3S 3C KD", "4H 4D 5S 5C KD") == "White wins. - with two pairs: 5"  # White has two pairs, 5s decide

def test_name_hand_category_three_of_a_kind():
    assert showdown("2H 2D 2S 9C KD", "3H 3D 5S 9C KD") == "Black wins. - with three of a kind"  # Black has three of a kind

def test_name_hand_category_straight():
    assert showdown("2H 3D 4S 5C 6D", "9H TH JH QH KH") == "White wins. - with straight"  # White has straight
    assert showdown("9H TH JH QH KH", "8H 9H TH JH QH") == "White wins. - with straight flush"  # White has straight flush

def test_name_hand_category_flush():
    assert showdown("2H 5H 8H KH AH", "2D 5D 8D KH AD") == "Black wins. - with flush"  # Black has flush
    assert showdown("2D 5D 8D KH AD", "2H 5H 8H KH AH") == "Black wins. - with flush"  # Black has flush

def test_name_hand_category_full_house():
    assert showdown("2H 2D 2S 3C 3D", "4H 4D 4S 3C 3D") == "White wins. - with full house: 4"  # White has full house

def test_name_hand_category_four_of_a_kind():
    assert showdown("2H 2D 2S 2C 3D", "3H 3D 3S 3C 4D") == "White wins. - with four of a kind: 3"  # White has four of a kind

def test_name_hand_category_straight_flush():
    assert showdown("2H 3H 4H 5H 6H", "9H TH JH QH KH") == "White wins. - with straight flush"  # White has straight flush

def test_showdown_black_wins():
    assert showdown("2H 3D 5S 9C KD", "AH KH QH JD TH") == "White wins. - with straight"  # White has a straight
    assert showdown("2H 2D 5S 9C KD", "3H 3D 5S 9C KD") == "White wins. - with pair: 3"  # White has pair of 3s

def test_showdown_white_wins():
    assert showdown("2H 3D 5S 9C KD", "2H 2D 5S 9C KD") == "Black wins. - with pair: 2"  # Black has pair of 2s
    assert showdown("2H 3D 5S 9C KD", "2H 2D 2S 3C 3D") == "White wins. - with full house: 2"  # White has full house

def test_showdown_tie():
    assert showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C KD") == "Tie."  # Both hands are identical

def test_showdown_flush_vs_full_house():
    assert showdown("2H 5H 8H KH AH", "3H 3D 3S 3C 4D") == "White wins. - with four of a kind: 3"  # White has four of a kind

def test_showdown_four_of_a_kind_vs_straight_flush():
    assert showdown("2H 2D 2S 2C 3D", "9H TH JH QH KH") == "White wins. - with straight flush"  # White has straight flush

def test_showdown_high_card_kicker():
    assert showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C KH") == "White wins. - with high card: King"  # White has higher kicker

def test_showdown_pair_kicker():
    assert showdown("2H 2D 5S 9C KD", "2H 2D 5S 9C 10D") == "Black wins. - with pair: 2"  # Black has the pair and higher kicker

def test_showdown_two_pairs():
    assert showdown("2H 2D 3S 3C KD", "4H 4D 5S 5C KD") == "White wins. - with two pairs: 5"  # White has two pairs, 5s decide

def test_showdown_three_of_a_kind():
    assert showdown("2H 2D 2S 5C KD", "3H 3D 3S 5C KD") == "White wins. - with three of a kind: 3"  # White has three of a kind

def test_showdown_full_house():
    assert showdown("2H 2D 2S 3C 3D", "4H 4D 4S 3C 3D") == "White wins. - with full house: 4"  # White has full house

def test_showdown_straight_flush():
    assert showdown("2H 3H 4H 5H 6H", "9H TH JH QH KH") == "White wins. - with straight flush"  # White has straight flush

def test_showdown_tie_different_suits():
    assert showdown("2H 3D 5S 9C KD", "2D 3H 5H 9D KC") == "Tie."  # Both hands have identical values