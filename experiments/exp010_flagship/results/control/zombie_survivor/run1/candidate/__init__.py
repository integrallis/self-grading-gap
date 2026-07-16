class Survivor:
    def __init__(self, name):
        self.name = name
        self.wounds = 0
        self.actions = 3
        self.equipment = []
        self.experience = 0
        self.update_level()

    def is_alive(self):
        return self.wounds < 2

    def take_wound(self):
        if self.is_alive():
            self.wounds += 1
        if not self.is_alive():
            return f"{self.name} is dead"

    def pick_up(self, item):
        if self.is_alive():
            max_capacity = 5 - self.wounds  # Reduce capacity by number of wounds
            if len(self.equipment) < max_capacity:
                self.equipment.append(item)
        else:
            return f"{self.name} is dead"

    def gain_experience(self, points):
        self.experience += points
        self.update_level()

    def update_level(self):
        if self.experience >= 43:
            self.level = "Red"
            self.available_skills = ["Hoard", "Sniper", "Tough"]
        elif self.experience >= 19:
            self.level = "Orange"
            self.available_skills = ["Hoard", "Sniper"]
        elif self.experience >= 7:
            self.level = "Yellow"
            self.actions = 4
            self.available_skills = []
        else:
            self.level = "Blue"
            self.available_skills = []

class Game:
    def __init__(self, start_time):
        self.start_time = start_time
        self.survivors = []
        self.history = [f"Game started at {start_time}"]

    def add_survivor(self, survivor):
        if survivor.name in [s.name for s in self.survivors]:
            return f"A survivor named '{survivor.name}' already exists"
        self.survivors.append(survivor)
        self.history.append(f"{survivor.name} joined the game")

    def is_over(self):
        return all(not s.is_alive() for s in self.survivors)

    @property
    def level(self):
        return max(s.level for s in self.survivors if s.is_alive()) if self.survivors else "Blue"