class Tower:
    def __init__(self, color, level):
        if level < 1 or level > 4:
            raise ValueError(f'tower level must be between 1 and 4, got {level}')
        self.color = color
        self.level = level

    def attack(self, jelly):
        if jelly.health <= 0:
            return 0
        if self.color == jelly.color:
            return random.randint(2, 5) if self.level == 1 else random.randint(5, 9)
        elif self.color == 'BlueRed':
            if jelly.color == 'Red':
                return random.randint(2, 4) if self.level == 2 else 0
            return 2
        else:
            return 0

class Jelly:
    def __init__(self, color, health):
        self.color = color
        self.health = health

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        if not self.is_alive():
            raise ValueError('Cannot attack a dead jelly')
        self.health = max(0, self.health - amount)

import random

def combat_round(towers, jellies):
    log = []
    for tower in towers:
        for jelly in jellies:
            if jelly.is_alive():
                damage = tower.attack(jelly)
                jelly.take_damage(damage)
                log.append({'tower': tower, 'jelly': jelly})
    return log
