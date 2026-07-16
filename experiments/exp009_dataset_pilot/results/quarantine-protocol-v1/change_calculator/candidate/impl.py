# candidate/impl.py

class CoinChangeMaker:
    def __init__(self):
        self.denominations = [25, 10, 5, 1]

    def make_change(self, amount):
        if amount == 0:
            return []
        
        coins = []
        for denomination in self.denominations:
            while amount >= denomination:
                coins.append(denomination)
                amount -= denomination
        return coins
