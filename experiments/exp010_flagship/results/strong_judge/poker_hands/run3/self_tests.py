from solution import read_hand, name_hand_category, decide_showdown

def test_read_hand_valid():
    assert read_hand("2H 3D 5S 9C KD") == ["2H", "3D", "5S", "9C", "KD"]
    assert read_hand("TH 2S 4C 8H JS") == ["TH", "2S", "4C", "8H", "JS"]
    assert read_hand("10H 2S 4C 8H JS") == ["10H", "2S", "4C", "8H", "JS"]  # valid 10 notation

def test_read_hand_invalid_length():
    assert read_hand("2H 3D 5S") == "a hand must contain exactly 5 cards"
    assert read_hand("2H 3D 5S 9C KD 6H") == "a hand must contain exactly 5 cards"

def test_read_hand_invalid_card_value():
    assert read_hand("1H 3D 5S 9C KD") == "invalid card: '1H'"
    assert read_hand("2H 3D 5S 9C 10Z") == "invalid card: '10Z'"

def test_read_hand_invalid_card_suit():
    assert read_hand("2H 3D 5S 9C 1Z") == "invalid card: '1Z'"

def test_read_hand_invalid_spacing():
    assert read_hand("2H 3D  5S 9C KD") == "a hand must contain exactly 5 cards"  # invalid due to double space

def test_name_hand_category_high_card():
    assert name_hand_category(["2H", "3D", "5S", "9C", "KD"]) == "high card"
    assert name_hand_category(["2H", "3D", "5S", "9C", "AH"]) == "high card"
    assert name_hand_category(["AH", "2D", "3S", "4C", "5H"]) == "high card"  # Ace high, not a straight

def test_name_hand_category_pair():
    assert name_hand_category(["2H", "2D", "5S", "9C", "KD"]) == "pair"
    assert name_hand_category(["3H", "3D", "5S", "9C", "KD"]) == "pair"

def test_name_hand_category_two_pairs():
    assert name_hand_category(["2H", "2D", "3S", "3C", "KD"]) == "two pairs"
    assert name_hand_category(["3H", "3D", "4S", "4C", "KD"]) == "two pairs"

def test_name_hand_category_three_of_a_kind():
    assert name_hand_category(["2H", "2D", "2S", "9C", "KD"]) == "three of a kind"
    assert name_hand_category(["3H", "3D", "3S", "9C", "KD"]) == "three of a kind"

def test_name_hand_category_straight():
    assert name_hand_category(["3H", "4D", "5S", "6C", "7H"]) == "straight"
    assert name_hand_category(["TH", "JH", "QH", "KH", "AH"]) == "straight flush"  # Ace high, all hearts
    assert name_hand_category(["2H", "3D", "4S", "5C", "6H"]) == "straight"  # valid straight

def test_name_hand_category_flush():
    assert name_hand_category(["2H", "4H", "6H", "8H", "TH"]) == "flush"
    assert name_hand_category(["3C", "5C", "7C", "9C", "JC"]) == "flush"

def test_name_hand_category_full_house():
    assert name_hand_category(["2H", "2D", "2S", "3C", "3D"]) == "full house"
    assert name_hand_category(["3H", "3D", "3S", "2C", "2D"]) == "full house"

def test_name_hand_category_four_of_a_kind():
    assert name_hand_category(["2H", "2D", "2S", "2C", "3D"]) == "four of a kind"
    assert name_hand_category(["3H", "3D", "3S", "3C", "4D"]) == "four of a kind"

def test_name_hand_category_straight_flush():
    assert name_hand_category(["3H", "4H", "5H", "6H", "7H"]) == "straight flush"
    assert name_hand_category(["TH", "JH", "QH", "KH", "AH"]) == "straight flush"

def test_decide_showdown_black_wins():
    assert decide_showdown("2H 3D 5S 9C KD", "2D 3H 5C 8S KS") == "Black wins. - with high card: 9"
    assert decide_showdown("2H 3H 5H 9H KH", "2D 2H 5C 5D 5H") == "White wins. - with full house"  # Black flush vs White full house

def test_decide_showdown_white_wins():
    assert decide_showdown("2H 3D 5S 9C KD", "3H 4D 5S 6C 7H") == "White wins. - with straight"
    assert decide_showdown("3H 3D 5S 9C KD", "3H 4D 5S 6C 7H") == "White wins. - with straight"

def test_decide_showdown_tie():
    assert decide_showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C KD") == "Tie."
    
def test_decide_showdown_high_card_comparison():
    assert decide_showdown("2H 3D 5S 9C KD", "2H 3D 5S 8C KH") == "Black wins. - with high card: 9"  # Black's highest card wins

def test_decide_showdown_pair_comparison():
    assert decide_showdown("2H 2D 5S 9C KD", "2H 2D 5S 8C KH") == "Black wins. - with pair: 9"  # Same pair, Black has higher kicker

def test_decide_showdown_different_pair_values():
    assert decide_showdown("8H 2D 5S 9C KD", "7H 3D 5S 9C KD") == "Black wins. - with pair: 8"  # Black has higher pair

def test_decide_showdown_two_pair_comparison():
    assert decide_showdown("2H 2D 3S 3C 5H", "4H 4D 3S 3C 5H") == "White wins. - with two pairs: 4"  # White has higher two pairs
    assert decide_showdown("2H 2D 3S 3C 5H", "2H 2D 5S 5C 3H") == "Black wins. - with two pairs: 2"  # Black has higher low pair

def test_decide_showdown_straight_comparison():
    assert decide_showdown("3H 4H 5H 6H 7H", "2D 3D 4D 5D 6D") == "Black wins. - with straight flush: 7"  # Black has higher straight flush

def test_decide_showdown_flush_comparison():
    assert decide_showdown("2H 4H 6H 8H TH", "2D 3D 5D 7D AD") == "White wins. - with flush: Ace"  # White has higher flush

def test_decide_showdown_four_of_a_kind_comparison():
    assert decide_showdown("2H 2D 2S 2C 3D", "3H 3D 3S 3C 4D") == "White wins. - with four of a kind: 3"  # White has higher four of a kind

def test_decide_showdown_straight_flush_comparison():
    assert decide_showdown("3H 4H 5H 6H 7H", "2H 2D 2S 2C 3D") == "Black wins. - with straight flush: 7"  # Black has straight flush

def test_decide_showdown_deciding_value_formatting():
    assert decide_showdown("2H 2D 2S 2C 3D", "2H 2D 2S 2C 4D") == "White wins. - with four of a kind: 4"  # Test for four of a kind with deciding value

    assert decide_showdown("TH 2D 3S 4C 5H", "9H 2D 3S 4C 5H") == "Black wins. - with high card: 10"  # Test for deciding value formatting for 10

    assert decide_showdown("KH 2D 3S 4C 5H", "TH 2D 3S 4C 5H") == "Black wins. - with high card: King"  # Test for deciding value formatting for King

    assert decide_showdown("AH 2D 3S 4C 5H", "KH 2D 3S 4C 5H") == "Black wins. - with high card: Ace"  # Test for deciding value formatting for Ace

def test_decide_showdown_tie_with_equal_values():
    assert decide_showdown("2H 2D 3S 3C 4H", "2S 2C 3D 3H 4D") == "Tie."  # Same cards, different suits