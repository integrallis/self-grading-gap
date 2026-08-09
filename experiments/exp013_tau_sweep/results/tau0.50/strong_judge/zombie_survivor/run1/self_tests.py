from solution import Survivor, Game
import datetime

def test_new_survivor():
    # A newly created survivor has a name, no wounds, is alive, can take three actions per turn,
    # carries nothing, has zero experience, and is at level Blue.
    survivor = Survivor("Alice")
    assert survivor.name == "Alice"
    assert survivor.wounds == 0
    assert survivor.is_alive is True
    assert survivor.actions == 3
    assert survivor.load == []
    assert survivor.experience == 0
    assert survivor.level == "Blue"

def test_survivor_wounds():
    survivor = Survivor("Bob")
    survivor.take_wound()  # First wound
    assert survivor.wounds == 1
    assert survivor.is_alive is True
    survivor.take_wound()  # Second wound
    assert survivor.wounds == 2
    assert survivor.is_alive is False
    survivor.take_wound()  # Third wound does nothing
    assert survivor.wounds == 2

def test_equipment_load():
    survivor = Survivor("Charlie")
    assert survivor.load == []

    # Pick up equipment
    survivor.pick_up("Weapon")
    assert survivor.load == ["Weapon"]
    
    survivor.pick_up("Medkit")
    assert survivor.load == ["Weapon", "Medkit"]

    survivor.pick_up("Axe")
    survivor.pick_up("Shield")
    survivor.pick_up("Food")
    assert survivor.load == ["Weapon", "Medkit", "Axe", "Shield", "Food"]
    
    # Picking up more than capacity
    result = survivor.pick_up("Armor")
    assert result == "Charlie cannot carry any more equipment"

def test_wounds_reduce_carrying_capacity():
    survivor = Survivor("David")
    survivor.take_wound()  # Wounds reduce capacity
    survivor.pick_up("Gun")
    survivor.pick_up("Knife")
    survivor.pick_up("Rope")
    survivor.pick_up("Canned Food")
    survivor.pick_up("First Aid Kit")
    assert survivor.load == ["Gun", "Knife", "Rope", "Canned Food"]

    # One more wound, capacity reduced
    survivor.take_wound()
    survivor.pick_up("Flashlight")  # Should discard Canned Food
    assert survivor.load == ["Gun", "Knife", "Rope"]  # Correct load after death
    assert survivor.pick_up("Flashlight") == "David is dead"  # Cannot pick up after death

def test_dead_survivor_cannot_pick_up_equipment():
    survivor = Survivor("Eve")
    survivor.take_wound()
    survivor.take_wound()  # Eve is now dead
    result = survivor.pick_up("Tent")
    assert result == "Eve is dead"

def test_experience_and_level_up():
    survivor = Survivor("Frank")
    assert survivor.experience == 0
    assert survivor.level == "Blue"
    
    survivor.kill_zombie()  # 1 kill
    assert survivor.experience == 1
    assert survivor.level == "Blue"
    
    for _ in range(6):  # 6 more kills
        survivor.kill_zombie()
    assert survivor.experience == 7
    assert survivor.level == "Yellow"

    for _ in range(11):  # 11 more kills to reach Orange
        survivor.kill_zombie()
    assert survivor.experience == 18
    assert survivor.level == "Yellow"

    survivor.kill_zombie()  # 1 more kill to reach Orange
    assert survivor.experience == 19
    assert survivor.level == "Orange"

    for _ in range(24):  # 24 more kills to reach Red
        survivor.kill_zombie()
    assert survivor.experience == 43
    assert survivor.level == "Red"

    survivor.kill_zombie()  # 1 more kill to reach second automatic +1 Action
    assert survivor.experience == 44
    assert survivor.actions == 4  # Actions remain 4 until 50 experience
    survivor.kill_zombie()  # 1 more kill to reach 50 experience
    assert survivor.experience == 50
    assert survivor.actions == 5  # Actions increase to 5 at 50 experience

def test_skills_unlocking():
    survivor = Survivor("Grace")
    for _ in range(7):  # Level up to Yellow
        survivor.kill_zombie()
    assert survivor.actions == 4  # +1 Action at Yellow
    assert survivor.skills == []

    for _ in range(11):  # Level up to Orange
        survivor.kill_zombie()
    assert survivor.skills == []  # No skills before level-up choice

    try:
        survivor.choose_skill("Hoard")  # Choose Hoard
    except Exception as e:
        assert str(e) == "Grace has no skill choice available"  # No choice available before Orange

    # Now reach Orange, choose Hoard
    survivor.choose_skill("Hoard")  
    assert survivor.skills == ["Hoard"]
    assert survivor.load == []  # Check if load remains empty until equipment is picked up
    assert survivor.max_capacity == 6  # Capacity increased

    survivor.choose_skill("Sniper")  # Choose Sniper
    assert survivor.skills == ["Hoard", "Sniper"]
    assert survivor.max_capacity == 6  # Hoard still allows 6 items

    try:
        survivor.choose_skill("Tough")  # Should raise an error
    except Exception as e:
        assert str(e) == "'Tough' is not an available skill choice"  # Skills should not change

def test_game_management():
    clock = datetime.datetime(2026, 1, 1, 12, 0, 0)
    game = Game(clock)  # Game starts with clock
    assert game.history[0] == f"Game started at {clock.isoformat()}"

    survivor = Survivor("Heidi")
    game.add_survivor(survivor)
    assert game.history == [f"Game started at {clock.isoformat()}", "Heidi joined the game"]
    
    result = game.add_survivor(survivor)  # Duplicate survivor
    assert result == "A survivor named 'Heidi' already exists"
    assert game.history == [f"Game started at {clock.isoformat()}", "Heidi joined the game"]
    
    survivor.take_wound()
    assert not game.is_over
    survivor.take_wound()
    assert game.is_over
    assert game.history[-1] == "The game has ended: all survivors died"

    # Check game level
    assert game.level == "Blue"

    survivor2 = Survivor("Jack")
    survivor3 = Survivor("Kate")
    game.add_survivor(survivor2)
    game.add_survivor(survivor3)

    # Make Jack and Kate kill zombies to change their levels
    for _ in range(7):
        survivor2.kill_zombie()
    for _ in range(18):
        survivor3.kill_zombie()
    
    assert game.level == "Yellow"  # Highest level is Yellow
    survivor3.take_wound()
    survivor3.take_wound()  # Kill Kate
    assert game.level == "Yellow"  # Still highest level is Yellow
    survivor2.take_wound()  # Kill Jack
    survivor2.take_wound()  # Now game should end
    assert game.is_over

    # Test join order
    survivor4 = Survivor("Liam")
    game.add_survivor(survivor4)
    assert game.history == [
        f"Game started at {clock.isoformat()}", 
        "Heidi joined the game", 
        "Jack joined the game", 
        "Kate joined the game", 
        "Liam joined the game"
    ]
    
    # Test dead joiner
    survivor5 = Survivor("Noah")
    survivor5.take_wound()
    survivor5.take_wound()  # Noah is dead
    game.add_survivor(survivor5)  # Should end the game
    assert game.history[-1] == "The game has ended: all survivors died"