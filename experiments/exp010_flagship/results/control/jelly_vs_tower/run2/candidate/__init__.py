class Tower:
    def __init__(self, color, level):
        if level < 1 or level > 4:
            raise ValueError(f"tower level must be between 1 and 4, got {level}")
        self.color = color
        self.level = level

    def attack(self, jelly):
        if jelly.color == self.color or (self.color == 'BlueRed' and jelly.color in ['Blue', 'Red']):
            if self.level == 1:
                return 2  # Minimum damage for level 1
            elif self.level == 2:
                return 5  # Minimum damage for level 2
            elif self.level == 3:
                return 9  # Minimum damage for level 3
            elif self.level == 4:
                return 12  # Minimum damage for level 4
        elif self.color == 'Blue':
            if jelly.color == 'Red':
                return 0  # Level 1 against Red
            elif self.level == 2:
                return 1  # Level 2 against Red
            elif self.level == 3:
                return 2  # Level 3 against Red
            elif self.level == 4:
                return 3  # Level 4 against Red
        elif self.color == 'Red':
            if jelly.color == 'Blue':
                return 0  # Level 1 against Blue
            elif self.level == 2:
                return 1  # Level 2 against Blue
            elif self.level == 3:
                return 2  # Level 3 against Blue
            elif self.level == 4:
                return 3  # Level 4 against Blue
        return 0  # No damage against other colors

class Jelly:
    def __init__(self, color, health):
        self.color = color
        self.health = health

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        if not self.is_alive():
            raise ValueError("Cannot attack a dead jelly")
        self.health -= amount

class Combat:
    def __init__(self, towers, jellies):
        self.towers = towers
        self.jellies = jellies

    def fight_round(self):
        log = []
        for tower in self.towers:
            for jelly in self.jellies:
                if jelly.is_alive():
                    damage = tower.attack(jelly)
                    jelly.take_damage(damage)
                    log.append({'tower': tower, 'jelly': jelly})
                    if not jelly.is_alive():
                        self.jellies.remove(jelly)
                    break
        return log
