def read_hand(hand):
    cards = hand.split()
    if len(cards) != 5:
        return 'a hand must contain exactly 5 cards'
    for card in cards:
        if card[0] not in '23456789TJQKA' or card[1] not in 'CDHS':
            return f'invalid card: \'{card}\''
    return cards


def name_hand_category(hand):
    cards = read_hand(hand)
    if isinstance(cards, str):
        return cards
    values = sorted([card[0] for card in cards], key=lambda x: '23456789TJQKA'.index(x))
    suits = [card[1] for card in cards]
    value_counts = {v: values.count(v) for v in set(values)}
    counts = sorted(value_counts.values(), reverse=True)
    is_flush = len(set(suits)) == 1
    is_straight = len(set(values)) == 5 and (max('23456789TJQKA'.index(v) for v in values) - min('23456789TJQKA'.index(v) for v in values) == 4)

    if is_straight and is_flush:
        return 'straight flush'
    if counts == [4, 1]:
        return 'four of a kind'
    if counts == [3, 2]:
        return 'full house'
    if is_flush:
        return 'flush'
    if is_straight:
        return 'straight'
    if counts == [3, 1, 1]:
        return 'three of a kind'
    if counts == [2, 2, 1]:
        return 'two pairs'
    if counts == [2, 1, 1, 1]:
        return 'pair'
    return 'high card'


def decide_showdown(black, white):
    hand_rankings = {'high card': 0, 'pair': 1, 'two pairs': 2, 'three of a kind': 3, 'straight': 4, 'flush': 5, 'full house': 6, 'four of a kind': 7, 'straight flush': 8}
    black_category = name_hand_category(black)
    white_category = name_hand_category(white)
    if isinstance(black_category, str):
        return black_category
    if isinstance(white_category, str):
        return white_category
    if hand_rankings[black_category] > hand_rankings[white_category]:
        return f'Black wins. - with {black_category}'
    elif hand_rankings[white_category] > hand_rankings[black_category]:
        return f'White wins. - with {white_category}'
    else:
        return 'Tie.'