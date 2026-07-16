class Survivor:
    def __init__(self, name):
        self.name = name
        self.wounds = 0
        self.alive = True
        self.actions = 3
        self.equipment = []
        self.experience = 0
        self.level = "Blue"
        self.carrying_capacity = 5

    def take_wound(self):
        if self.alive:
            self.wounds += 1
            if self.wounds >= 2:
                self.alive = False
            self.update_game_history(f"{self.name} was wounded")

    def can_carry(self):
        return len(self.equipment) < (self.carrying_capacity - (self.wounds // 2))

    def pick_up(self, item):
        if not self.alive:
            return f"{self.name} is dead"
        if self.can_carry():
            self.equipment.append(item)
        else:
            if len(self.equipment) > 0:
                self.equipment.pop(0)
            self.equipment.append(item)
            return f"{self.name} cannot carry any more equipment"

    def kill_zombie(self):
        self.experience += 1
        if self.experience >= 7:
            self.level = "Orange"
            self.actions = 4
        elif self.experience >= 4:
            self.level = "Yellow"
            self.actions = 4
        else:
            self.level = "Blue"

    def unlock_skills(self):
        if self.level == "Orange":
            return ["Hoard", "Sniper"]
        return []

    def choose_skill(self, skill):
        if skill == "Hoard" and self.carrying_capacity == 5:
            self.carrying_capacity += 2
            return f"Skill {skill} chosen"

    def update_game_history(self, action):
        # Placeholder for game history update
        pass

class Game:
    def __init__(self, start_time):
        self.history = [f"Game started at {start_time}"]
        self.survivors = []

    def add_survivor(self, survivor):
        self.survivors.append(survivor)
        self.history.append(f"{survivor.name} joined the game")

    def is_over(self):
        if all(not survivor.alive for survivor in self.survivors):
            self.history.append("The game has ended: all survivors died")
            return True
        return False

    def update_history(self, action):
        self.history.append(action)