def make_change(amount):
    coins = []
    denominations = [25, 10, 5, 1]
    for coin in denominations:
        while amount >= coin:
            coins.append(coin)
            amount -= coin
    return coins