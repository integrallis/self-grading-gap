# test_poker.py

from solution import read_hand, hand_category, showdown

def test_read_hand_valid():
    assert read_hand("2H 3D 5S 9C KD") == ["2H", "3D", "5S", "9C", "KD"]  # Valid hand
    assert read_hand("TH JH QH KH AH") == ["TH", "JH", "QH", "KH", "AH"]  # Valid hand
    assert read_hand("10H JH QH KH AH") == ["10H", "JH", "QH", "KH", "AH"]  # Valid hand with '10'

def test_read_hand_invalid_card():
    assert read_hand("1Z 3D 5S 9C KD") == "invalid card: '1Z'"  # Invalid card
    assert read_hand("2H 3D 5S 9C 10X") == "invalid card: '10X'"  # Invalid card
    assert read_hand("2H 3D 5S 9C KZ") == "invalid card: 'KZ'"  # Invalid card

def test_read_hand_invalid_card_count():
    assert read_hand("2H 3D 5S 9C") == "a hand must contain exactly 5 cards"  # Less than 5 cards
    assert read_hand("2H 3D 5S 9C KD 6H") == "a hand must contain exactly 5 cards"  # More than 5 cards

def test_read_hand_invalid_value():
    assert read_hand("1H 2D 3S 4C 5H") == "invalid card: '1H'"  # Invalid card value

def test_hand_category_high_card():
    assert hand_category(["2H", "3D", "5S", "9C", "KD"]) == "high card"  # No pairs or straights

def test_hand_category_pair():
    assert hand_category(["2H", "2D", "5S", "9C", "KD"]) == "pair"  # Single pair

def test_hand_category_two_pairs():
    assert hand_category(["2H", "2D", "5S", "5C", "KD"]) == "two pairs"  # Two pairs

def test_hand_category_three_of_a_kind():
    assert hand_category(["2H", "2D", "2S", "9C", "KD"]) == "three of a kind"  # Three of a kind

def test_hand_category_straight():
    assert hand_category(["2H", "3D", "4S", "5C", "6H"]) == "straight"  # Straight

def test_hand_category_flush():
    assert hand_category(["2H", "4H", "6H", "8H", "KH"]) == "flush"  # Flush

def test_hand_category_full_house():
    assert hand_category(["2H", "2D", "2S", "5C", "5H"]) == "full house"  # Full house

def test_hand_category_four_of_a_kind():
    assert hand_category(["2H", "2D", "2S", "2C", "5H"]) == "four of a kind"  # Four of a kind

def test_hand_category_straight_flush():
    assert hand_category(["2H", "3H", "4H", "5H", "6H"]) == "straight flush"  # Straight flush

def test_hand_category_ace_low():
    assert hand_category(["AH", "2D", "3S", "4C", "5H"]) == "high card"  # Ace-low should not count as straight

def test_showdown_black_wins():
    assert showdown("2H 3D 5S 9C KD", "2H 2D 5S 9C KD") == "White wins. - with pair: 2"  # Black has a high card vs White's pair

def test_showdown_white_wins():
    assert showdown("2H 3D 5S 9C KD", "3H 3D 5S 9C KD") == "White wins. - with pair: 3"  # White has a higher pair

def test_showdown_tie():
    assert showdown("2H 3D 5S 9C KD", "2H 3D 5S 9C KD") == "Tie."  # Both hands are equal

def test_showdown_high_card():
    assert showdown("2H 3D 5S 9C KD", "2C 3H 5D 8H KH") == "Black wins. - with high card: 9"  # Black has a higher card

def test_showdown_full_house_beats_flush():
    assert showdown("3H 3D 3S 5C 5H", "2H 4H 6H 8H KH") == "Black wins. - with full house"  # Full house vs flush

def test_showdown_straight_flush_beats_four_of_a_kind():
    assert showdown("3H 4H 5H 6H 7H", "2H 2D 2S 2C 5H") == "Black wins. - with straight flush"  # Straight flush vs four of a kind

def test_showdown_pair_versus_pair():
    assert showdown("3H 3D 5S 9C KD", "2H 2D 5S 9C KD") == "Black wins. - with pair: 3"  # Black's higher pair wins

def test_showdown_pair_versus_pair_tiebreaker():
    assert showdown("3H 3D 5S 9C AH", "3H 3D 5S 9C KH") == "Tie."  # Equal pairs, same kickers

def test_showdown_two_pair_comparison():
    assert showdown("5H 5D 3S 3C 2H", "5H 5D 4S 4C AH") == "White wins. - with two pairs: 4"  # White's high pair wins

def test_showdown_straight_comparison():
    assert showdown("2H 3D 4S 5C 6H", "3H 4D 5S 6C 7H") == "White wins. - with straight: 7"  # White has a higher straight

def test_showdown_flush_comparison():
    assert showdown("2H 4H 6H 8H KH", "3H 5H 7H 9H AH") == "White wins. - with flush: Ace"  # White has a higher flush

def test_showdown_four_of_a_kind_comparison():
    assert showdown("2H 2D 2S 2C KH", "3H 3D 3S 3C AH") == "White wins. - with four of a kind: 3"  # White has four of a kind

def test_showdown_four_of_a_kind_tiebreaker():
    assert showdown("3H 3D 3S 3C KH", "2H 2D 2S 2C AH") == "Black wins. - with four of a kind: 3"  # Black has higher quad

def test_showdown_straight_flush_comparison():
    assert showdown("3H 4H 5H 6H 7H", "7H 8H 9H TH JH") == "White wins. - with straight flush: Jack"  # White has higher straight flush

def test_showdown_tie_with_different_suits():
    assert showdown("2H 2D 3S 4C 5H", "2C 2S 3H 4D 5D") == "Tie."  # Both hands are equal in value