# test_poker.py

from solution import read_hand, name_hand_category, decide_showdown
import pytest

def test_read_hand_valid():
    read_hand("2H 3D 5S 9C KD")  # Valid hand, no return value expected

def test_read_hand_invalid_card_value():
    with pytest.raises(ValueError, match="invalid card: '1H'"):
        read_hand("1H 3D 5S 9C KD")  # Invalid card value

def test_read_hand_invalid_card_suit():
    with pytest.raises(ValueError, match="invalid card: '9X'"):
        read_hand("2H 3D 5S 9X KD")  # Invalid card suit

def test_read_hand_too_few_cards():
    with pytest.raises(ValueError, match="a hand must contain exactly 5 cards"):
        read_hand("2H 3D 5S")  # Too few cards

def test_read_hand_too_many_cards():
    with pytest.raises(ValueError, match="a hand must contain exactly 5 cards"):
        read_hand("2H 3D 5S 9C KD 10H")  # Too many cards

def test_read_hand_valid_ten_as_T():
    read_hand("TH 3D 5S 9C KD")  # Valid hand with 'T'

def test_read_hand_valid_ten_as_10():
    read_hand("10H 3D 5S 9C KD")  # Valid hand with '10'

def test_read_hand_invalid_spacing():
    with pytest.raises(ValueError, match="a hand must contain exactly 5 cards"):
        read_hand("2H  3D 5S 9C KD")  # Invalid spacing

def test_name_hand_category_high_card():
    assert name_hand_category("2H 3D 5S 9C KD") == "high card"  # No significant combinations

def test_name_hand_category_pair():
    assert name_hand_category("2H 2D 5S 9C KD") == "pair"  # Pair of 2s

def test_name_hand_category_two_pairs():
    assert name_hand_category("2H 2D 5S 5C KD") == "two pairs"  # Two pairs: 2s and 5s

def test_name_hand_category_three_of_a_kind():
    assert name_hand_category("2H 2D 2S 9C KD") == "three of a kind"  # Three of a kind: 2s

def test_name_hand_category_straight():
    assert name_hand_category("4H 5D 6S 3C 2D") == "straight"  # 2-3-4-5-6 straight

def test_name_hand_category_flush():
    assert name_hand_category("2H 5H 8H KH QH") == "flush"  # All hearts, but not consecutive

def test_name_hand_category_full_house():
    assert name_hand_category("2H 2D 2S 5C 5D") == "full house"  # Three 2s and a pair of 5s

def test_name_hand_category_four_of_a_kind():
    assert name_hand_category("2H 2D 2S 2C 5D") == "four of a kind"  # Four 2s

def test_name_hand_category_straight_flush():
    assert name_hand_category("4H 5H 6H 7H 8H") == "straight flush"  # Straight flush

def test_name_hand_category_ace_high_card():
    assert name_hand_category("AH 2D 3S 4C 5H") == "high card"  # Ace-high, not a straight

def test_decide_showdown_black_wins():
    assert decide_showdown("2H 2D 5S 9C KD", "2H 3D 5S 9C KD") == "Black wins. - with pair: 2"  # Black has a pair

def test_decide_showdown_white_wins_flush():
    assert decide_showdown("2H 2D 5S 9C KD", "2H 4H 5H 9H KH") == "White wins. - with flush: King"  # White has a flush

def test_decide_showdown_tie():
    assert decide_showdown("2H 2D 5S 9C KD", "2H 2D 5S 9C KD") == "Tie."  # Both hands are equal

def test_decide_showdown_full_house_beats_straight_flush():
    assert decide_showdown("2H 2D 2S 5C 5D", "3H 4H 5H 6H 7H") == "White wins. - with straight flush"  # Straight flush beats full house

def test_decide_showdown_straight_flush_beats_four_of_a_kind():
    assert decide_showdown("9H 9D 9S 9C 5H", "4H 5H 6H 7H 8H") == "White wins. - with straight flush"  # Straight flush beats four of a kind

def test_decide_showdown_high_card_comparison():
    assert decide_showdown("KH KD 9H 8S 7C", "KS KH 9C 8D 6H") == "Black wins. - with pair: 9"  # High card comparison

def test_decide_showdown_pair_comparison_higher_pair():
    assert decide_showdown("4H 4D 3S 2C 5H", "3H 3D 2S 2C AH") == "Black wins. - with pair: 4"  # Higher pair

def test_decide_showdown_pair_comparison_equal_pair_kicker():
    assert decide_showdown("4H 4D 5S 2C 3H", "4H 4D 5H 2C AH") == "White wins. - with pair: Ace"  # Equal pair, kicker decides

def test_decide_showdown_two_pair_higher_pair():
    assert decide_showdown("4H 4D 5S 5C 3H", "6H 6D 3S 3C AH") == "White wins. - with two pairs: 6"  # Higher pair wins

def test_decide_showdown_two_pair_equal_high_pair():
    assert decide_showdown("4H 4D 5S 5C 3H", "4H 4D 5C 5S AH") == "White wins. - with two pairs: Ace"  # Equal high pair, lower pair decides

def test_decide_showdown_straight_comparison():
    assert decide_showdown("5H 6H 7H 8H 9H", "9D 10D JD QD KD") == "White wins. - with straight flush: King"  # Higher straight flush wins

def test_decide_showdown_flush_high_card_comparison():
    assert decide_showdown("2H 5H 8H KH 9H", "3C 4C 5C 6C 7C") == "Black wins. - with flush: King"  # Flush comparison

def test_decide_showdown_four_of_a_kind_comparison():
    assert decide_showdown("9H 9D 9S 9C 5H", "9H 9D 9S 8C 7H") == "Black wins. - with four of a kind: 9"  # Four of a kind comparison

def test_decide_showdown_deciding_value_formatting():
    assert decide_showdown("KH KD 9H 8S 7C", "KS KH 9C 8D 6H") == "Black wins. - with pair: 9"  # Valid formatting for deciding value

def test_decide_showdown_tie_with_different_suits():
    assert decide_showdown("2H 3D 4S 5C 6H", "2C 3H 4D 5S 6C") == "Tie."  # Same values, different suits