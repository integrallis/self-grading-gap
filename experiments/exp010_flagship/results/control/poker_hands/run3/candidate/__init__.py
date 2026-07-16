def read_hand(hand):
    cards = hand.split()
    if len(cards) != 5:
        return "a hand must contain exactly 5 cards"
    for card in cards:
        if len(card) != 2 or card[0] not in '23456789TJQKA' or card[1] not in 'CDHS':
            return f"invalid card: '{card}'"
    return cards

def name_hand_category(hand):
    values = {v: i for i, v in enumerate('23456789TJQKA', start=2)}
    cards = read_hand(hand)
    if isinstance(cards, str): return cards  # Forward invalid input
    counts = {v: 0 for v in values}
    suits = {}
    for card in cards:
        value, suit = card[0], card[1]
        counts[value] += 1
        if suit not in suits:
            suits[suit] = 0
        suits[suit] += 1
    value_counts = sorted(counts.values(), reverse=True)
    is_flush = len(suits) == 1
    consecutive_values = sorted(values[v] for v in counts if counts[v] > 0)
    is_straight = len(consecutive_values) == 5 and (consecutive_values[-1] - consecutive_values[0] == 4)

    if is_flush and is_straight:
        return "straight flush"
    if 4 in value_counts:
        return "four of a kind"
    if 3 in value_counts and 2 in value_counts:
        return "full house"
    if is_flush:
        return "flush"
    if is_straight:
        return "straight"
    if 3 in value_counts:
        return "three of a kind"
    if value_counts.count(2) == 2:
        return "two pairs"
    if 2 in value_counts:
        return "pair"
    return "high card"

def decide_showdown(black_hand, white_hand):
    black_category = name_hand_category(black_hand)
    white_category = name_hand_category(white_hand)
    if isinstance(black_category, str): return black_category  # Forward invalid input
    if isinstance(white_category, str): return white_category

    ranks = {'high card': 0, 'pair': 1, 'two pairs': 2, 'three of a kind': 3, 'straight': 4, 'flush': 5, 'full house': 6, 'four of a kind': 7, 'straight flush': 8}
    if ranks[black_category] > ranks[white_category]:
        return f"Black wins. - with {black_category}"
    elif ranks[black_category] < ranks[white_category]:
        return f"White wins. - with {white_category}"
    else:
        return "Tie."