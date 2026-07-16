import random

class Tower:
    def __init__(self, color, level):
        if level < 1 or level > 4:
            raise ValueError(f"tower level must be between 1 and 4, got {level}")
        self.color = color
        self.level = level

    def attack(self, jelly):
        if jelly.health <= 0:
            return 0
        if self.color == jelly.color:
            damage = random.randint(2 + self.level, 5 + self.level)  # Adjusted to meet requirements
            return damage
        elif self.color in ['BlueRed', 'RedBlue'] and jelly.color in ['Blue', 'Red']:
            return 2  # Fixed damage for dual tower against pure jelly
        elif jelly.color in ['BlueRed', 'RedBlue']:
            damage = self.level  # Less for dual jelly
            return random.randint(2, max(damage, 0) + 1)  # Ensure non-negative return
        return 0

class Jelly:
    def __init__(self, color, health):
        self.color = color
        self.health = health

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        if not self.is_alive():
            raise ValueError("Jelly is dead and cannot be attacked.")
        self.health = max(0, self.health - amount)

def attack_round(towers, jellies):
    log = []
    for tower, jelly in zip(towers, jellies):
        if jelly.is_alive():
            damage = tower.attack(jelly)
            jelly.take_damage(damage)
            log.append({'tower': tower.color, 'jelly': jelly.color})
    return log
