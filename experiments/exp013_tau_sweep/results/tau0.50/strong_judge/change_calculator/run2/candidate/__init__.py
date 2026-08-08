def make_change(amount):
    coins = [25, 10, 5, 1]
    change = []
    for coin in coins:
        while amount >= coin:
            change.append(coin)
            amount -= coin
    return change