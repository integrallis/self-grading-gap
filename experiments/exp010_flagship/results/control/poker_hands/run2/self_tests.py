from solution import read_hand, name_hand_category, decide_showdown

def test_read_hand_valid():
    assert read_hand("2H 3D 5S 9C KD") == ["2H", "3D", "5S", "9C", "KD"]  # Valid hand

def test_read_hand_too_few_cards():
    assert read_hand("2H 3D 5S") == "a hand must contain exactly 5 cards"  # Less than 5 cards

def test_read_hand_too_many_cards():
    assert read_hand("2H 3D 5S 9C KD 6H") == "a hand must contain exactly 5 cards"  # More than 5 cards

def test_read_hand_invalid_card_value():
    assert read_hand("1H 3D 5S 9C KD") == "invalid card: '1H'"  # Invalid card value

def test_read_hand_invalid_card_suit():
    assert read_hand("2H 3D 5S 9Z KD") == "invalid card: '9Z'"  # Invalid card suit

def test_name_hand_category_high_card():
    assert name_hand_category("2H 3D 5S 9C KD") == "high card"  # No pairs or straights

def test_name_hand_category_pair():
    assert name_hand_category("2H 2D 5S 9C KD") == "pair"  # One pair

def test_name_hand_category_two_pairs():
    assert name_hand_category("2H 2D 5S 5C KD") == "two pairs"  # Two pairs

def test_name_hand_category_three_of_a_kind():
    assert name_hand_category("2H 2D 2S 9C KD") == "three of a kind"  # Three of a kind

def test_name_hand_category_straight():
    assert name_hand_category("2H 3D 4S 5C 6D") == "straight"  # Straight

def test_name_hand_category_flush():
    assert name_hand_category("2H 4H 5H 9H KH") == "flush"  # Flush

def test_name_hand_category_full_house():
    assert name_hand_category("2H 2D 2S 5C 5D") == "full house"  # Full house

def test_name_hand_category_four_of_a_kind():
    assert name_hand_category("2H 2D 2S 2C 5D") == "four of a kind"  # Four of a kind

def test_name_hand_category_straight_flush():
    assert name_hand_category("2H 3H 4H 5H 6H") == "straight flush"  # Straight flush

def test_name_hand_category_invalid():
    assert name_hand_category("1H 2D 3S 4C 5D") == "invalid card: '1H'"  # Invalid card value

def test_decide_showdown_black_wins():
    assert decide_showdown("2H 3D 5S 9C KD", "2H 2D 5S 9C KD") == "Black wins. - with pair: 2"  # Black has a pair over high card

def test_decide_showdown_white_wins():
    assert decide_showdown("2H 2D 5S 9C KD", "2H 3D 5S 9C KD") == "White wins. - with high card: 9"  # White has a high card over a pair

def test_decide_showdown_tie():
    assert decide_showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C KD") == "Tie."  # Both hands are equal

def test_decide_showdown_black_full_house():
    assert decide_showdown("2H 2D 2S 5C 5D", "3H 3D 4S 5C 6D") == "Black wins. - with full house"  # Black full house beats white straight

def test_decide_showdown_white_straight_flush():
    assert decide_showdown("2H 3D 4S 5C 6D", "3H 4H 5H 6H 7H") == "White wins. - with straight flush"  # White straight flush beats black straight