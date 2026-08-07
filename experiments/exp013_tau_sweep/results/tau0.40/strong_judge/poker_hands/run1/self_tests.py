from solution import read_hand, decide_showdown

def test_read_hand_five_cards():
    assert read_hand("2H 3D 5S 9C KD") == ["2H", "3D", "5S", "9C", "KD"]  # valid hand

def test_read_hand_invalid_card_unknown_value():
    assert read_hand("1H 3D 5S 9C KD") == "invalid card: '1H'"  # invalid card with unknown value

def test_read_hand_invalid_card_unknown_suit():
    assert read_hand("2H 3D 5S 9C 2Z") == "invalid card: '2Z'"  # invalid card with unknown suit

def test_read_hand_more_than_five_cards():
    assert read_hand("2H 3D 5S 9C KD 6H") == "a hand must contain exactly 5 cards"  # too many cards

def test_read_hand_fewer_than_five_cards():
    assert read_hand("2H 3D 5S") == "a hand must contain exactly 5 cards"  # too few cards

def test_read_hand_valid_ten_values():
    assert read_hand("TH 3D 5S 9C KD") == ["TH", "3D", "5S", "9C", "KD"]  # valid hand with '10' as 'T'
    assert read_hand("10H 3D 5S 9C KD") == ["10H", "3D", "5S", "9C", "KD"]  # valid hand with '10' as '10'

def test_name_hand_category_high_card():
    assert name_hand_category(["2H", "3D", "5S", "9C", "KD"]) == "high card"  # no pairs or straights

def test_name_hand_category_pair():
    assert name_hand_category(["2H", "2D", "5S", "9C", "KD"]) == "pair"  # one pair

def test_name_hand_category_two_pairs():
    assert name_hand_category(["2H", "2D", "5S", "5C", "KD"]) == "two pairs"  # two pairs

def test_name_hand_category_three_of_a_kind():
    assert name_hand_category(["2H", "2D", "2S", "9C", "KD"]) == "three of a kind"  # three of a kind

def test_name_hand_category_straight():
    assert name_hand_category(["2H", "3D", "4S", "5C", "6D"]) == "straight"  # consecutive values

def test_name_hand_category_flush():
    assert name_hand_category(["2H", "4H", "5H", "9H", "KH"]) == "flush"  # same suit

def test_name_hand_category_full_house():
    assert name_hand_category(["2H", "2D", "2S", "5C", "5D"]) == "full house"  # three of a kind and a pair

def test_name_hand_category_four_of_a_kind():
    assert name_hand_category(["2H", "2D", "2S", "2C", "5D"]) == "four of a kind"  # four of a kind

def test_name_hand_category_straight_flush():
    assert name_hand_category(["2H", "3H", "4H", "5H", "6H"]) == "straight flush"  # straight of the same suit

def test_name_hand_category_invalid_straight_with_ace():
    assert name_hand_category(["AS", "2H", "3D", "4C", "5S"]) == "high card"  # A,2,3,4,5 is not a straight

def test_decide_showdown_black_wins():
    assert decide_showdown("2H 3D 5S 9C KD", "2C 3C 5C 9C KC") == "White wins. - with flush"  # flush beats high card

def test_decide_showdown_white_wins():
    assert decide_showdown("2H 3D 5S 9C KD", "3C 4C 5C 6C 7C") == "White wins. - with straight flush"  # straight flush beats high card

def test_decide_showdown_tie():
    assert decide_showdown("2H 3D 5S 9C KD", "2D 3S 5H 9C KD") == "Tie."  # both hands are equal

def test_decide_showdown_higher_pair():
    assert decide_showdown("2H 2D 5S 9C KD", "3C 3D 5C 9C KC") == "White wins. - with pair: 3"  # higher pair wins

def test_decide_showdown_equal_pairs_high_card_decides():
    assert decide_showdown("2H 2D 5S 9C KD", "2C 2S 5D 9D KS") == "Tie."  # equal pairs, highest kickers are equal

def test_decide_showdown_two_pairs_deciding_value():
    assert decide_showdown("2H 2D 5S 5C KD", "3C 3D 5C 5D KS") == "Black wins. - with two pairs: 5"  # equal high pairs, lower pair decides

def test_decide_showdown_straight_deciding_value():
    assert decide_showdown("2H 3D 4S 5C 6D", "3C 4C 5C 6C 7C") == "White wins. - with straight flush"  # straight flush comparison

def test_decide_showdown_flush_deciding_value():
    assert decide_showdown("2H 4H 5H 9H KH", "3C 4C 5C 6C 7C") == "White wins. - with straight flush"  # straight flush comparison

def test_decide_showdown_full_house_over_flush():
    assert decide_showdown("2H 2D 2S 5C 5D", "3H 4H 5H 6H 7H") == "White wins. - with straight flush"  # full house vs straight flush

def test_decide_showdown_straight_flush_over_four_of_a_kind():
    assert decide_showdown("2H 2D 2S 2C 5D", "3C 4C 5C 6C 7C") == "White wins. - with straight flush"  # straight flush vs four of a kind

def test_decide_showdown_high_card_kicker_fallback():
    assert decide_showdown("2H 3D 5S 9C KD", "2D 3H 5C 9D KS") == "Tie."  # equal high cards

def test_decide_showdown_pair_kicker_fallback():
    assert decide_showdown("2H 2D 5S 9C KD", "2C 2S 5D 9D 10H") == "Black wins. - with pair: 2"  # equal pairs, kickers decide

def test_decide_showdown_faithful_high_card_fallback():
    assert decide_showdown("2H 3D 5S 9C KD", "2D 3H 5C 8D KS") == "Black wins. - with high card: 9"  # high card comparison, 9 beats 8

def test_decide_showdown_three_of_a_kind():
    assert decide_showdown("2H 2D 2S 5C 9D", "3C 3D 3S 4C 5D") == "Black wins. - with three of a kind: 2"  # three of a kind comparison

def test_decide_showdown_full_house_vs_three_of_a_kind():
    assert decide_showdown("2H 2D 2S 5C 5D", "3C 3D 3S 4C 5D") == "Black wins. - with full house"  # full house vs three of a kind