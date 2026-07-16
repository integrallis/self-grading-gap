def read_hand(hand_string):
    cards = hand_string.split()
    if len(cards) != 5:
        return 'a hand must contain exactly 5 cards'
    for card in cards:
        if len(card) != 2 or card[0] not in '23456789TJQKA' or card[1] not in 'CDHS':
            return f'invalid card: \'{card}\''
    return cards


def hand_category(hand_string):
    values = {r: i for i, r in enumerate('23456789TJQKA', start=2)}
    cards = read_hand(hand_string)
    if isinstance(cards, str):
        return cards  # return error message if invalid

    value_counts = {v: 0 for v in values.values()}
    for card in cards:
        value_counts[values[card[0]]] += 1

    counts = sorted(value_counts.values(), reverse=True)
    is_flush = len(set(card[1] for card in cards)) == 1
    sorted_values = sorted([v for v, count in value_counts.items() if count > 0], reverse=True)
    is_straight = len(sorted_values) == 5 and (sorted_values[0] - sorted_values[4] == 4)

    if is_flush and is_straight:
        return 'straight flush'
    elif counts == [4, 1]:
        return 'four of a kind'
    elif counts == [3, 2]:
        return 'full house'
    elif is_flush:
        return 'flush'
    elif is_straight:
        return 'straight'
    elif counts == [3, 1, 1]:
        return 'three of a kind'
    elif counts == [2, 2, 1]:
        return 'two pairs'
    elif counts == [2, 1, 1, 1]:
        return 'pair'
    else:
        return 'high card'


def showdown(hand1, hand2):
    category1 = hand_category(hand1)
    category2 = hand_category(hand2)
    if isinstance(category1, str):
        return category1  # if invalid hand
    if isinstance(category2, str):
        return category2  # if invalid hand

    rank_order = ['high card', 'pair', 'two pairs', 'three of a kind', 'straight', 'flush', 'full house', 'four of a kind', 'straight flush']
    score1 = rank_order.index(category1)
    score2 = rank_order.index(category2)

    if score1 > score2:
        return f'Black wins. - with {category1}: {max_hand_value(hand1)}'
    elif score2 > score1:
        return f'White wins. - with {category2}: {max_hand_value(hand2)}'
    else:
        return 'Tie.'


def max_hand_value(hand_string):
    values = {r: i for i, r in enumerate('23456789TJQKA', start=2)}
    cards = read_hand(hand_string)
    if isinstance(cards, str):
        return cards  # return error message if invalid
    return max(values[card[0]] for card in cards)