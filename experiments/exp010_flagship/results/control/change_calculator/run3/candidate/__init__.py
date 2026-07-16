def make_change(amount):
    coins = []
    for coin in [25, 10, 5, 1]:
        while amount >= coin:
            coins.append(coin)
            amount -= coin
    return coins