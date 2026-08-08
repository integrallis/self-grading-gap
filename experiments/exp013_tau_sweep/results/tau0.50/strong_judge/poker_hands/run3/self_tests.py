from solution import decide_showdown, name_hand_category

def test_read_hand_invalid_card_count():
    assert read_hand("2H 3D 5S") == "a hand must contain exactly 5 cards"
    assert read_hand("2H 3D 5S 9C KD 6H") == "a hand must contain exactly 5 cards"

def test_read_hand_invalid_card_value_or_suit():
    assert read_hand("1Z 3D 5S 9C KD") == "invalid card: '1Z'"
    assert read_hand("2H 3D 5S 9C 1Z") == "invalid card: '1Z'"
    assert read_hand("1H 3D 5S 9C KD") == "invalid card: '1H'"
    assert read_hand("2H 3D 5S 9C 2Z") == "invalid card: '2Z'"

def test_name_hand_category_high_card():
    assert name_hand_category(["2H", "3D", "5S", "9C", "KD"]) == "high card"
    assert name_hand_category(["2H", "3D", "5S", "9C", "KH"]) == "high card"
    assert name_hand_category(["AH", "2D", "3S", "4C", "5H"]) == "high card"  # Ace high, not straight

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
    assert name_hand_category(["2H", "3D", "4S", "5C", "6H"]) == "straight"
    assert name_hand_category(["AH", "2D", "3S", "4C", "5H"]) == "high card"  # Ace-high, not straight

def test_name_hand_category_flush():
    assert name_hand_category(["2H", "5H", "8H", "10H", "KH"]) == "flush"
    assert name_hand_category(["3D", "5D", "7D", "9D", "KD"]) == "flush"

def test_name_hand_category_full_house():
    assert name_hand_category(["2H", "2D", "2S", "3C", "3D"]) == "full house"
    assert name_hand_category(["3H", "3D", "3S", "2C", "2D"]) == "full house"

def test_name_hand_category_four_of_a_kind():
    assert name_hand_category(["2H", "2D", "2S", "2C", "3D"]) == "four of a kind"
    assert name_hand_category(["3H", "3D", "3S", "3C", "4D"]) == "four of a kind"

def test_name_hand_category_straight_flush():
    assert name_hand_category(["2H", "3H", "4H", "5H", "6H"]) == "straight flush"
    assert name_hand_category(["10D", "JD", "QD", "KD", "AD"]) == "straight flush"

def test_decide_showdown_black_wins():
    assert decide_showdown("2H 3D 5S 9C KD", "2D 3H 5H 9H KH") == "Tie."
    assert decide_showdown("2H 2D 5S 9C KD", "3D 3H 5H 9H KH") == "White wins. - with pair: 3"
    assert decide_showdown("3H 4D 5S 9C KD", "2D 3H 5H 9H KH") == "Black wins. - with high card: 4"  # 4 beats 3
    assert decide_showdown("4H 5D 6S 7C 8H", "2H 3H 4H 5H 6H") == "White wins. - with straight flush"

def test_decide_showdown_white_wins():
    assert decide_showdown("2H 3D 5S 9C KD", "3D 3H 5H 9H KH") == "White wins. - with pair: 3"
    assert decide_showdown("2H 3D 5S 9C KD", "10H JH QH KH AH") == "White wins. - with straight flush"

def test_decide_showdown_tie():
    assert decide_showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C KD") == "Tie."

def test_decide_showdown_two_pairs():
    assert decide_showdown("2H 2D 3H 3D 4S", "2S 2C 3C 3S 5H") == "Black wins. - with two pairs: 3"  # 3 over 2
    assert decide_showdown("2H 2D 3H 3D 4S", "2S 2C 4C 4S 5H") == "White wins. - with two pairs: 4"  # 4 over 3

def test_decide_showdown_three_of_a_kind():
    assert decide_showdown("2H 2D 2S 3C 4D", "3H 3D 3S 2C 4D") == "White wins. - with three of a kind: 3"  # 3 over 2
    assert decide_showdown("3H 3D 3S 2C 4D", "3H 3D 3S 2C 5D") == "White wins. - with three of a kind: 3"  # Kicker 5 over 4

def test_decide_showdown_straight():
    assert decide_showdown("2H 3H 4H 5H 6H", "3H 4H 5H 6H 7H") == "White wins. - with straight: 7"  # 7 over 6
    assert decide_showdown("9H TH JH QH KH", "2H 3H 4H 5H 6H") == "Black wins. - with straight: K"  # K over 6

def test_decide_showdown_flush():
    assert decide_showdown("2H 5H 8H AH KH", "2D 5D 8D 10D JH") == "Black wins. - with flush: Ace"  # Ace over 10
    assert decide_showdown("2H 5H 8H AH KH", "3D 5D 8D 10D JH") == "Black wins. - with flush: Ace"  # Ace over J

def test_decide_showdown_full_house():
    assert decide_showdown("2H 2D 2S 3C 3D", "3H 3D 3S 2C 2D") == "Tie."  # Equal full house

def test_decide_showdown_four_of_a_kind():
    assert decide_showdown("2H 2D 2S 2C 3D", "3H 3D 3S 3C 4D") == "White wins. - with four of a kind: 3"  # 3 over 2
    assert decide_showdown("3H 3D 3S 3C 4D", "3H 3D 3S 3C 5D") == "White wins. - with four of a kind: 3"  # Kicker 5 over 4

def test_decide_showdown_straight_flush():
    assert decide_showdown("2H 3H 4H 5H 6H", "3H 4H 5H 6H 7H") == "White wins. - with straight flush: 7"  # 7 over 6
    assert decide_showdown("3H 4H 5H 6H 7H", "2H 3H 4H 5H 6H") == "Black wins. - with straight flush: 6"  # 6 over 5