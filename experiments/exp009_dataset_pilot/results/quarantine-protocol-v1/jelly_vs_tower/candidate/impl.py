import random

class Tower:
    DAMAGE_TABLE = {
        'Blue': {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
        'Red': {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
        'BlueRed': {1: (2, 2), 2: (2, 4), 3: (4, 6), 4: (6, 8)}
    }

    def __init__(self, color, level):
        if level < 1 or level > 4:
            raise ValueError(f"tower level must be between 1 and 4, got {level}")
        self.color = color
        self.level = level

    def attack(self, jelly, random_source):
        if not jelly.is_alive():
            raise ValueError("cannot attack a dead jelly")
        
        damage = self.calculate_damage(jelly)
        jelly.take_damage(damage)
        return damage

    def calculate_damage(self, jelly):
        if self.color == jelly.color:
            damage_range = Tower.DAMAGE_TABLE[self.color][self.level]
            return random.randint(*damage_range)
        elif (self.color == 'BlueRed'):
            blue_damage = Tower.DAMAGE_TABLE['Blue'][self.level]
            red_damage = Tower.DAMAGE_TABLE['Red'][self.level]
            return max(random.randint(*blue_damage), random.randint(*red_damage))
        else:
            return Tower.DAMAGE_TABLE[self.color][self.level][1]  # Fixed damage


class Jelly:
    def __init__(self, color, health):
        self.color = color
        self.health = health

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        if not self.is_alive():
            raise ValueError("cannot damage a dead jelly")
        self.health -= damage


class CombatRound:
    def __init__(self, towers, jellies, random_source):
        self.towers = towers
        self.jellies = jellies
        self.random_source = random_source
        self.log = []

    def fight(self):
        for tower in self.towers:
            for jelly in self.jellies:
                if jelly.is_alive():
                    damage = tower.attack(jelly, self.random_source)
                    self.log.append(f"{tower.color} Tower attacks {jelly.color} Jelly for {damage} damage.")
                    break  # Move to the next tower after one attack
        self.jellies = [jelly for jelly in self.jellies if jelly.is_alive()]


class Combat:
    def __init__(self, towers, jellies, random_source):
        self.towers = towers
        self.jellies = jellies
        self.random_source = random_source

    def start(self):
        while any(jelly.is_alive() for jelly in self.jellies):
            round = CombatRound(self.towers, self.jellies, self.random_source)
            round.fight()
            yield round.log
