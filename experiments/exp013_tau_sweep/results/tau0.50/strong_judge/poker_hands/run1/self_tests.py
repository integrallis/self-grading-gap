import pytest
from solution import read_hand, name_hand_category, decide_showdown

# US-1: Reading hands in card notation
def test_read_hand_valid():
    assert read_hand("2H 3D 5S 9C KD") == ["2H", "3D", "5S", "9C", "KD"]

def test_read_hand_valid_ten_as_T():
    assert read_hand("TH 3D 5S 9C KD") == ["TH", "3D", "5S", "9C", "KD"]

def test_read_hand_valid_ten_as_10():
    assert read_hand("10H 3D 5S 9C KD") == ["10H", "3D", "5S", "9C", "KD"]

def test_read_hand_invalid_card_value():
    assert read_hand("1H 3D 5S 9C KD") == "invalid card: '1H'"

def test_read_hand_invalid_card_suit():
    assert read_hand("2H 3D 5S 9A KD") == "invalid card: '9A'"

def test_read_hand_incorrect_number_of_cards():
    assert read_hand("2H 3D 5S") == "a hand must contain exactly 5 cards"

def test_read_hand_too_many_cards():
    assert read_hand("2H 3D 5S 9C KD 10H") == "a hand must contain exactly 5 cards"

# US-2: Naming the hand category
def test_name_hand_category_high_card():
    assert name_hand_category(["2H", "3D", "5S", "9C", "KD"]) == "high card"

def test_name_hand_category_pair():
    assert name_hand_category(["2H", "2D", "5S", "9C", "KD"]) == "pair"

def test_name_hand_category_two_pairs():
    assert name_hand_category(["2H", "2D", "5S", "5C", "KD"]) == "two pairs"

def test_name_hand_category_three_of_a_kind():
    assert name_hand_category(["2H", "2D", "2S", "9C", "KD"]) == "three of a kind"

def test_name_hand_category_straight():
    assert name_hand_category(["4H", "5D", "6S", "3C", "7D"]) == "straight"

def test_name_hand_category_flush():
    assert name_hand_category(["2H", "4H", "6H", "8H", "KH"]) == "flush"

def test_name_hand_category_full_house():
    assert name_hand_category(["2H", "2D", "2S", "5C", "5D"]) == "full house"

def test_name_hand_category_four_of_a_kind():
    assert name_hand_category(["2H", "2D", "2S", "2C", "KD"]) == "four of a kind"

def test_name_hand_category_straight_flush():
    assert name_hand_category(["3H", "4H", "5H", "6H", "7H"]) == "straight flush"

def test_name_hand_category_invalid_straight_with_ace():
    assert name_hand_category(["AH", "2D", "3S", "4C", "5D"]) == "high card"

# US-3: Deciding a showdown
def test_decide_showdown_black_wins_higher_category():
    assert decide_showdown("2H 3D 5S 9C KD", "2H 2D 5S 9C KD") == "White wins. - with pair"

def test_decide_showdown_white_wins_higher_category():
    assert decide_showdown("2H 2D 5S 9C KD", "3H 3D 5S 9C KD") == "White wins. - with pair: 3"

def test_decide_showdown_black_wins_higher_category_two_pairs():
    assert decide_showdown("2H 2D 5S 5C KD", "3H 3D 5S 5C KD") == "White wins. - with two pairs: 3"

def test_decide_showdown_black_wins_higher_category_three_of_a_kind():
    assert decide_showdown("3H 3D 3S 5C KD", "2H 2D 5S 5C KD") == "Black wins. - with three of a kind: 3"

def test_decide_showdown_black_wins_higher_category_straight():
    assert decide_showdown("3H 4D 5S 6C 7D", "2H 2D 5S 5C KD") == "Black wins. - with straight: 7"

def test_decide_showdown_black_wins_higher_category_flush():
    assert decide_showdown("2H 4H 6H 8H KH", "2D 3D 5D 7D 9D") == "Black wins. - with flush: King"

def test_decide_showdown_equal_categories_high_card():
    assert decide_showdown("2H 3D 5S 9C KD", "2C 3H 5D 9S KH") == "Tie."

def test_decide_showdown_equal_categories_high_card_with_different_kickers():
    assert decide_showdown("2H 3D 5S 9C KD", "2C 3H 5D 9S 2H") == "White wins. - with pair: 2"

def test_decide_showdown_equal_categories_with_ties():
    assert decide_showdown("KH 9D 5S 3C 2H", "KH 9C 5D 3H 2S") == "Tie."

def test_decide_showdown_pair_equal_pair_different_kickers():
    assert decide_showdown("8H 8D 5S 3C 2H", "8C 8S 5D 4H 2S") == "Black wins. - with pair: 8"

def test_decide_showdown_two_pair_equal_high_pair():
    assert decide_showdown("8H 8D 5S 5C 2H", "8C 8S 5D 4H 2S") == "Black wins. - with two pairs: 5"

def test_decide_showdown_straight_higher_top_card():
    assert decide_showdown("3H 4D 5S 6C 7D", "3H 4D 5S 6C 8D") == "White wins. - with straight: 8"

def test_decide_showdown_flush_higher_card():
    assert decide_showdown("2H 4H 6H 8H KH", "2D 4D 6D 8D 10D") == "White wins. - with flush: 10"

def test_decide_showdown_four_of_a_kind_higher_quad():
    assert decide_showdown("9H 9D 9S 9C 8H", "8H 8D 8S 8C KH") == "Black wins. - with four of a kind: 9"

def test_decide_showdown_deciding_value_ace():
    assert decide_showdown("AH 2D 3S 4C 5H", "KH 2D 3S 4C 5H") == "Black wins. - with high card: Ace"

def test_decide_showdown_deciding_value_king():
    assert decide_showdown("KH 2D 3S 4C 5H", "QH 2D 3S 4C 5H") == "Black wins. - with high card: King"

def test_decide_showdown_deciding_value_ten():
    assert decide_showdown("TH 2D 3S 4C 5H", "9H 2D 3S 4C 5H") == "Black wins. - with high card: 10"

def test_decide_showdown_exact_tie():
    assert decide_showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C KD") == "Tie."