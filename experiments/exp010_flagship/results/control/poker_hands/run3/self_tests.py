from solution import read_hand, name_hand_category, decide_showdown

def test_read_hand_valid():
    assert read_hand("2H 3D 5S 9C KD") == ["2H", "3D", "5S", "9C", "KD"]
    assert read_hand("TH JD QS KH AS") == ["TH", "JD", "QS", "KH", "AS"]

def test_read_hand_invalid_card_value():
    assert read_hand("1H 2D 3S 4C 5H") == "invalid card: '1H'"

def test_read_hand_invalid_card_suit():
    assert read_hand("2H 3D 5S 9Z KD") == "invalid card: '9Z'"

def test_read_hand_too_few_cards():
    assert read_hand("2H 3D 5S") == "a hand must contain exactly 5 cards"

def test_read_hand_too_many_cards():
    assert read_hand("2H 3D 5S 9C KD 6H") == "a hand must contain exactly 5 cards"

def test_name_hand_category_high_card():
    assert name_hand_category("2H 3D 5S 9C KD") == "high card"
    assert name_hand_category("TH JD QS KH AS") == "high card"

def test_name_hand_category_pair():
    assert name_hand_category("2H 2D 5S 9C KD") == "pair"
    assert name_hand_category("TH JD TH KH AS") == "pair"

def test_name_hand_category_two_pairs():
    assert name_hand_category("2H 2D 3S 3C KD") == "two pairs"
    assert name_hand_category("TH JD TH KH JD") == "two pairs"

def test_name_hand_category_three_of_a_kind():
    assert name_hand_category("2H 2D 2S 9C KD") == "three of a kind"
    assert name_hand_category("TH JD TH KH TH") == "three of a kind"

def test_name_hand_category_straight():
    assert name_hand_category("2H 3D 4S 5C 6H") == "straight"
    assert name_hand_category("9H TH JH QH KH") == "straight"

def test_name_hand_category_flush():
    assert name_hand_category("2H 4H 5H 7H 9H") == "flush"
    assert name_hand_category("2D 4D 5D 7D 9D") == "flush"

def test_name_hand_category_full_house():
    assert name_hand_category("2H 2D 2S 3C 3D") == "full house"
    assert name_hand_category("TH TH TH JD JD") == "full house"

def test_name_hand_category_four_of_a_kind():
    assert name_hand_category("2H 2D 2S 2C 3D") == "four of a kind"
    assert name_hand_category("TH TH TH TH JD") == "four of a kind"

def test_name_hand_category_straight_flush():
    assert name_hand_category("2H 3H 4H 5H 6H") == "straight flush"
    assert name_hand_category("9S TS JS QS KS") == "straight flush"

def test_decide_showdown_black_wins():
    assert decide_showdown("2H 3D 4S 5C 6H", "2H 2D 3S 3C KD") == "Black wins. - with three of a kind"
    assert decide_showdown("TH JD TH KH AS", "2H 2D 3S 3C KD") == "Black wins. - with pair: 10"

def test_decide_showdown_white_wins():
    assert decide_showdown("2H 3D 4S 5C 6H", "TH JD TH KH AS") == "White wins. - with pair: 10"
    assert decide_showdown("2H 3D 4S 5C 6H", "2H 2D 3S 3C KD") == "White wins. - with full house"

def test_decide_showdown_tie():
    assert decide_showdown("2H 3D 4S 5C 6H", "2H 3D 4S 5C 6H") == "Tie."

def test_decide_showdown_high_card_decision():
    assert decide_showdown("2H 3D 4S 5C 6H", "3H 4D 5S 6C 7H") == "White wins. - with high card: 7"
    assert decide_showdown("9H TH JH QH KH", "9D TH JH QH KH") == "Tie."

def test_decide_showdown_flush_decision():
    assert decide_showdown("2H 4H 5H 7H 9H", "2D 4D 5D 7D 9D") == "Black wins. - with flush: 9"
    assert decide_showdown("2H 4H 5H 7H 9H", "3H 4H 5H 6H 7H") == "White wins. - with flush: 7"