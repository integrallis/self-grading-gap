class Survivor:
    def __init__(self, name):
        self.name = name
        self.wounds = 0
        self.alive = True
        self.actions = 3
        self.equipment = []
        self.experience = 0
        self.level = "Blue"
        self.skills = []

    def take_wound(self):
        if self.alive:
            self.wounds += 1
            if self.wounds >= 2:
                self.alive = False

    def can_carry(self):
        return 5 - self.wounds

    def pick_up(self, item):
        if not self.alive:
            raise ValueError(f"{self.name} is dead")
        if len(self.equipment) >= self.can_carry():
            self.equipment.pop(0)  # Discard the oldest item
        self.equipment.append(item)

    def kill_zombie(self):
        self.experience += 1
        self.check_level_up()

    def check_level_up(self):
        if self.experience >= 7:
            self.level = "Yellow"
            self.actions = 4
        if self.experience >= 19:
            self.unlock_skills()

    def unlock_skills(self):
        return ["Hoard", "Sniper"]

    def choose_skill(self, skill):
        if skill not in self.unlock_skills():
            raise ValueError(f"'{skill}' is not an available skill choice")
        self.skills.append(skill)
        if skill == "Hoard":
            self.actions += 1
            self.equipment.append("Item")  # Increase carrying capacity to 6

class Game:
    def __init__(self):
        from datetime import datetime
        self.start_time = datetime.now()
        self.history = [f"Game started at {self.start_time.isoformat()}"]
        self.survivors = []

    def add_survivor(self, survivor):
        self.survivors.append(survivor)
        self.history.append(f"{survivor.name} joined the game")

    def is_over(self):
        return all(not survivor.alive for survivor in self.survivors)

    @property
    def level(self):
        return "Blue" if all(survivor.level == 'Blue' for survivor in self.survivors) else "Yellow"