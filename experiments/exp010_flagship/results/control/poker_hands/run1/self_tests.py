from solution import read_hand, hand_category, showdown

def test_read_hand_valid():
    assert read_hand("2H 3D 5S 9C KD") == ["2H", "3D", "5S", "9C", "KD"]
    assert read_hand("TH JH QH KH AH") == ["TH", "JH", "QH", "KH", "AH"]

def test_read_hand_invalid_card_count():
    assert read_hand("2H 3D 5S 9C") == "a hand must contain exactly 5 cards"
    assert read_hand("2H 3D 5S 9C KD 6H") == "a hand must contain exactly 5 cards"

def test_read_hand_invalid_card_value():
    assert read_hand("1H 3D 5S 9C KD") == "invalid card: '1H'"
    assert read_hand("2H 3D 5S 9C ZD") == "invalid card: 'ZD'"

def test_hand_category_high_card():
    assert hand_category("2H 3D 5S 9C KD") == "high card"
    assert hand_category("2H 2D 5S 9C KD") == "pair"
    assert hand_category("2H 2D 3S 3C KD") == "two pairs"
    assert hand_category("3H 3D 3S 9C KD") == "three of a kind"
    assert hand_category("2H 3H 4H 5H 6H") == "flush"
    assert hand_category("2H 3D 4S 5C 6H") == "straight"
    assert hand_category("3H 3D 3S 2C 2D") == "full house"
    assert hand_category("4H 4D 4S 4C 2H") == "four of a kind"
    assert hand_category("5H 6H 7H 8H 9H") == "straight flush"

def test_showdown_black_wins():
    assert showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C 10D") == "Black wins. - with high card: King"
    assert showdown("3H 3D 5S 9C KD", "2H 2D 5S 9C KD") == "Black wins. - with three of a kind"

def test_showdown_white_wins():
    assert showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C AH") == "White wins. - with high card: Ace"
    assert showdown("2H 3D 5S 9C KD", "3H 3D 5S 9C KD") == "White wins. - with pair: King"

def test_showdown_tie():
    assert showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C KD") == "Tie."