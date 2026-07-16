# test_zombie_survival_game.py

from solution import Survivor, Game

def test_new_survivor():
    survivor = Survivor("Alice")
    assert survivor.name == "Alice"
    assert survivor.wounds == 0
    assert survivor.is_alive() is True
    assert survivor.actions == 3
    assert survivor.equipment == []
    assert survivor.experience == 0
    assert survivor.level == "Blue"

def test_survivor_take_wound():
    survivor = Survivor("Bob")
    survivor.take_wound()
    assert survivor.wounds == 1
    assert survivor.is_alive() is True

def test_survivor_take_two_wounds():
    survivor = Survivor("Charlie")
    survivor.take_wound()
    survivor.take_wound()
    assert survivor.wounds == 2
    assert survivor.is_alive() is False

def test_survivor_take_more_than_two_wounds():
    survivor = Survivor("Diana")
    survivor.take_wound()
    survivor.take_wound()
    survivor.take_wound()  # Ignored
    assert survivor.wounds == 2
    assert survivor.is_alive() is False

def test_survivor_carry_equipment():
    survivor = Survivor("Eve")
    survivor.pick_up("Knife")
    survivor.pick_up("Axe")
    assert survivor.equipment == ["Knife", "Axe"]  # Two in hand
    survivor.pick_up("Shield")
    assert survivor.equipment == ["Knife", "Axe", "Shield"]  # One in reserve
    survivor.pick_up("Helmet")
    assert survivor.equipment == ["Knife", "Axe", "Shield", "Helmet"]  # Second in reserve
    survivor.pick_up("Armor")
    assert survivor.equipment == ["Knife", "Axe", "Shield", "Helmet", "Armor"]  # Third in reserve

def test_survivor_exceed_carry_capacity():
    survivor = Survivor("Frank")
    for i in range(6):  # Trying to pick up 6 items
        survivor.pick_up(f"Item {i}")
    assert len(survivor.equipment) == 5  # Should have only 5 items
    assert survivor.equipment[0] == "Item 0"  # First item in hand
    assert survivor.equipment[1] == "Item 1"  # Second item in hand
    assert survivor.equipment[2] == "Item 2"  # First reserve
    assert survivor.equipment[3] == "Item 3"  # Second reserve
    assert survivor.equipment[4] == "Item 4"  # Third reserve

def test_survivor_carry_capacity_reduction_by_wounds():
    survivor = Survivor("Grace")
    survivor.take_wound()
    survivor.pick_up("Axe")
    survivor.pick_up("Shield")
    survivor.pick_up("Helmet")  # This should succeed
    survivor.pick_up("Armor")  # This should succeed
    survivor.pick_up("Boots")  # This should succeed
    survivor.pick_up("Extra Item")  # This should fail
    assert len(survivor.equipment) == 5  # Carrying 5 items still

def test_dead_survivor_cannot_pick_up_equipment():
    survivor = Survivor("Hank")
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    result = survivor.pick_up("Weapon")
    assert result == "Hank is dead"

def test_game_initialization():
    game = Game("2026-01-01T12:00:00")
    assert len(game.survivors) == 0
    assert game.history == ["Game started at 2026-01-01T12:00:00"]

def test_survivor_join_game():
    game = Game("2026-01-01T12:00:00")
    survivor = Survivor("Ivy")
    game.add_survivor(survivor)
    assert len(game.survivors) == 1
    assert game.history == [
        "Game started at 2026-01-01T12:00:00",
        "Ivy joined the game"
    ]

def test_unique_survivor_names():
    game = Game("2026-01-01T12:00:00")
    survivor1 = Survivor("Jack")
    game.add_survivor(survivor1)
    survivor2 = Survivor("Jack")
    result = game.add_survivor(survivor2)
    assert result == "A survivor named 'Jack' already exists"

def test_game_ends_when_all_dead():
    game = Game("2026-01-01T12:00:00")
    survivor1 = Survivor("Kate")
    game.add_survivor(survivor1)
    survivor1.take_wound()
    survivor1.take_wound()  # Now dead
    assert game.is_over() is True

def test_game_level_tracking():
    game = Game("2026-01-01T12:00:00")
    survivor = Survivor("Liam")
    game.add_survivor(survivor)
    survivor.gain_experience(7)  # Level up to Yellow
    assert game.level == "Yellow"
    survivor.gain_experience(19)  # Level up to Orange
    assert game.level == "Orange"
    survivor.gain_experience(43)  # Level up to Red
    assert game.level == "Red"

def test_survivor_skill_unlocked_at_yellow():
    survivor = Survivor("Mia")
    survivor.gain_experience(7)  # Level up to Yellow
    assert survivor.actions == 4  # +1 Action skill granted

def test_survivor_skill_choice_at_orange():
    survivor = Survivor("Noah")
    survivor.gain_experience(19)  # Level up to Orange
    # Assume we can choose skills Hoard and Sniper
    assert survivor.available_skills == ["Hoard", "Sniper"]  # Check available skills

def test_survivor_skill_choice_at_red():
    survivor = Survivor("Olivia")
    survivor.gain_experience(43)  # Level up to Red
    # Assume we can choose skills Hoard, Sniper, and Tough
    assert survivor.available_skills == ["Hoard", "Sniper", "Tough"]  # Check available skills