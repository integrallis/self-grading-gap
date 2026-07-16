from solution import Survivor, Game

def test_new_survivor():
    survivor = Survivor("Alice")
    assert survivor.name == "Alice"
    assert survivor.wounds == 0
    assert survivor.alive is True
    assert survivor.actions == 3
    assert survivor.equipment == []
    assert survivor.experience == 0
    assert survivor.level == "Blue"

def test_wounds_tracking():
    survivor = Survivor("Bob")
    survivor.take_wound()
    assert survivor.wounds == 1
    assert survivor.alive is True
    survivor.take_wound()
    assert survivor.wounds == 2
    assert survivor.alive is False
    survivor.take_wound()  # Should be ignored
    assert survivor.wounds == 2

def test_equipment_load():
    survivor = Survivor("Charlie")
    assert survivor.can_carry() is True

    survivor.pick_up("Knife")
    assert survivor.equipment == ["Knife"]
    assert survivor.can_carry() is True

    survivor.pick_up("Pistol")
    survivor.pick_up("Axe")
    survivor.pick_up("Rope")
    survivor.pick_up("Medkit")
    assert survivor.equipment == ["Knife", "Pistol", "Axe", "Rope", "Medkit"]
    assert survivor.can_carry() is True

    # Should refuse additional equipment
    result = survivor.pick_up("Flashlight")
    assert result == "Charlie cannot carry any more equipment"
    assert survivor.equipment == ["Knife", "Pistol", "Axe", "Rope", "Medkit"]

def test_equipment_load_with_wounds():
    survivor = Survivor("Diana")
    survivor.take_wound()  # Now has 1 wound
    survivor.pick_up("Sword")
    survivor.pick_up("Shield")  # Should fill in hand first
    survivor.pick_up("Bow")
    survivor.pick_up("Arrow")
    survivor.pick_up("Trap")
    assert survivor.equipment == ["Sword", "Shield", "Bow", "Arrow"]
    assert survivor.can_carry() is True  # 4 pieces max due to 1 wound

    survivor.pick_up("Grenade")
    assert survivor.equipment == ["Shield", "Bow", "Arrow", "Grenade"]  # "Sword" was discarded
    assert survivor.can_carry() is True

def test_dead_survivor_cannot_pick_up_equipment():
    survivor = Survivor("Eve")
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    result = survivor.pick_up("Gun")
    assert result == "Eve is dead"
    assert survivor.equipment == []

def test_experience_and_level_up():
    survivor = Survivor("Frank")
    for _ in range(6):
        survivor.kill_zombie()
    assert survivor.experience == 6
    assert survivor.level == "Blue"

    survivor.kill_zombie()  # Should reach level up
    assert survivor.experience == 7
    assert survivor.level == "Yellow"

def test_skill_unlocking():
    survivor = Survivor("Grace")
    assert survivor.actions == 3  # Starts with 3 actions
    survivor.kill_zombie()  # To reach Yellow
    survivor.kill_zombie()
    survivor.kill_zombie()
    survivor.kill_zombie()
    survivor.kill_zombie()
    survivor.kill_zombie()
    survivor.kill_zombie()
    assert survivor.actions == 4  # Now 4 actions after reaching Yellow

def test_skill_choice():
    survivor = Survivor("Hank")
    survivor.kill_zombie()  # To reach Yellow
    survivor.kill_zombie()
    survivor.kill_zombie()
    survivor.kill_zombie()
    survivor.kill_zombie()
    survivor.kill_zombie()
    survivor.kill_zombie()
    survivor.kill_zombie()  # To reach Orange
    skills = survivor.unlock_skills()  # Should be Hoard and Sniper
    assert skills == ["Hoard", "Sniper"]

    result = survivor.choose_skill("Hoard")
    assert result == "Skill Hoard chosen"
    assert survivor.carrying_capacity == 6  # Capacity increased

def test_game_history():
    game = Game("2026-01-01T12:00:00")
    assert game.history == ["Game started at 2026-01-01T12:00:00"]

    survivor = Survivor("Ivy")
    game.add_survivor(survivor)
    assert game.history[-1] == "Ivy joined the game"
    
    survivor.take_wound()
    assert game.history[-1] == "Ivy was wounded"
    
    survivor.kill_zombie()
    assert survivor.experience == 1  # Experience increase
    assert game.history == ["Game started at 2026-01-01T12:00:00", "Ivy joined the game", "Ivy was wounded"]

def test_game_end_condition():
    game = Game("2026-01-01T12:00:00")
    survivor1 = Survivor("Jack")
    survivor2 = Survivor("Kara")
    game.add_survivor(survivor1)
    game.add_survivor(survivor2)
    
    survivor1.take_wound()
    survivor1.take_wound()  # Jack dies
    survivor2.take_wound()
    survivor2.take_wound()  # Kara dies

    assert game.is_over() is True
    assert game.history[-1] == "The game has ended: all survivors died"