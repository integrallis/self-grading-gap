def make_change(amount):
    coins = [25, 10, 5, 1]
    result = []
    for coin in coins:
        while amount >= coin:
            result.append(coin)
            amount -= coin
    return result
