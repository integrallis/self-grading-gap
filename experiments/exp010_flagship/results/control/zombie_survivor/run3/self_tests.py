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

def test_wound_survivor():
    survivor = Survivor("Bob")
    survivor.take_wound()
    assert survivor.wounds == 1
    assert survivor.alive is True
    survivor.take_wound()
    assert survivor.wounds == 2
    assert survivor.alive is False
    survivor.take_wound()  # This should not increase the wound count
    assert survivor.wounds == 2

def test_equipment_capacity():
    survivor = Survivor("Charlie")
    assert survivor.can_carry() == 5
    for i in range(5):
        survivor.pick_up(f"Item{i}")
    assert survivor.can_carry() == 5
    assert survivor.equipment == ["Item0", "Item1", "Item2", "Item3", "Item4"]
    with pytest.raises(ValueError, match="Charlie cannot carry any more equipment"):
        survivor.pick_up("Item5")

def test_equipment_with_wounds():
    survivor = Survivor("Dave")
    survivor.take_wound()
    assert survivor.can_carry() == 4
    survivor.pick_up("Item1")
    survivor.pick_up("Item2")
    survivor.pick_up("Item3")
    survivor.pick_up("Item4")
    assert survivor.equipment == ["Item1", "Item2", "Item3", "Item4"]
    survivor.pick_up("Item5")  # This should discard the last one to fit
    assert survivor.equipment == ["Item2", "Item3", "Item4", "Item5"]

def test_dead_survivor_cannot_pick_up_equipment():
    survivor = Survivor("Eve")
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    with pytest.raises(ValueError, match="Eve is dead"):
        survivor.pick_up("Item1")

def test_experience_and_level_up():
    survivor = Survivor("Frank")
    for _ in range(7):
        survivor.kill_zombie()  # Each kill gives 1 experience
    assert survivor.experience == 7
    assert survivor.level == "Yellow"

def test_skills_unlocked():
    survivor = Survivor("Grace")
    assert survivor.actions == 3
    survivor.experience = 7  # Manually setting for testing
    survivor.check_level_up()
    assert survivor.actions == 4  # "+1 Action" at Yellow
    with pytest.raises(ValueError, match="Grace has no skill choice available"):
        survivor.choose_skill("Hoard")

    survivor.experience = 19  # Manually setting for testing
    survivor.check_level_up()
    skills = survivor.unlock_skills()
    assert skills == ["Hoard", "Sniper"]

def test_choose_skill():
    survivor = Survivor("Hank")
    survivor.experience = 19  # Manually setting for testing
    survivor.check_level_up()
    survivor.choose_skill("Hoard")
    assert survivor.skills == ["Hoard"]
    assert survivor.can_carry() == 6  # Hoard increases carrying capacity

    with pytest.raises(ValueError, match="'Sniper' is not an available skill choice"):
        survivor.choose_skill("Sniper")

def test_game_creation():
    game = Game()
    assert game.history == ["Game started at " + game.start_time.isoformat()]
    assert game.survivors == []

def test_game_with_survivor():
    game = Game()
    survivor = Survivor("Ivy")
    game.add_survivor(survivor)
    assert game.survivors == [survivor]
    assert "Ivy joined the game" in game.history

def test_game_end_condition():
    game = Game()
    survivor1 = Survivor("Jack")
    survivor2 = Survivor("Kathy")
    game.add_survivor(survivor1)
    game.add_survivor(survivor2)
    
    survivor1.take_wound()
    survivor1.take_wound()  # Jack dies
    survivor2.take_wound()
    survivor2.take_wound()  # Kathy dies
    assert game.is_over() is True
    assert "The game has ended: all survivors died" in game.history

def test_game_level():
    game = Game()
    survivor = Survivor("Leo")
    game.add_survivor(survivor)
    survivor.kill_zombie()
    assert game.level == "Blue"
    for _ in range(6):  # Level up to Yellow
        survivor.kill_zombie()
    assert game.level == "Yellow"