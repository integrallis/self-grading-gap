from solution import Survivor, Game
from datetime import datetime

# Use a fixed clock for deterministic timestamp
fixed_clock = datetime(2026, 1, 1, 12, 0, 0)

def test_new_survivor():
    survivor = Survivor("Alice")
    # A newly created survivor has a name, no wounds, is alive, can take three actions per turn, carries nothing, has zero experience, and is at level Blue.
    assert survivor.name == "Alice"
    assert survivor.wounds == 0
    assert survivor.is_alive is True
    assert survivor.actions == 3
    assert survivor.equipment == []
    assert survivor.experience == 0
    assert survivor.level == "Blue"
    assert survivor.skills == []  # No skills initially

def test_survivor_wounds():
    survivor = Survivor("Bob")
    survivor.take_wound()
    # One wound leaves a survivor alive
    assert survivor.wounds == 1
    assert survivor.is_alive is True
    survivor.take_wound()
    # The second wound kills them
    assert survivor.wounds == 2
    assert survivor.is_alive is False
    survivor.take_wound()
    # Wounds inflicted past death are ignored
    assert survivor.wounds == 2

def test_equipment_load():
    survivor = Survivor("Charlie")
    survivor.pick_up_equipment("Baseball Bat")
    survivor.pick_up_equipment("Knife")
    survivor.pick_up_equipment("Rations")
    survivor.pick_up_equipment("Medkit")
    survivor.pick_up_equipment("Flashlight")
    # An unwounded survivor can carry at most five pieces
    assert survivor.equipment == ["Baseball Bat", "Knife", "Rations", "Medkit", "Flashlight"]

    result = survivor.pick_up_equipment("Axe")
    # Further pick-up is refused with an error
    assert result == "Charlie cannot carry any more equipment"
    assert survivor.equipment == ["Baseball Bat", "Knife", "Rations", "Medkit", "Flashlight"]

    survivor.take_wound()
    survivor.pick_up_equipment("Axe")
    # Each wound reduces carrying capacity by one and discards the most recently acquired reserve item
    assert survivor.equipment == ["Baseball Bat", "Knife", "Rations", "Medkit"]  # "Flashlight" is discarded
    result = survivor.pick_up_equipment("Axe")
    # Further pick-up is refused with an error
    assert result == "Charlie cannot carry any more equipment"

def test_dead_survivor_cannot_pick_up_equipment():
    survivor = Survivor("Diana")
    survivor.take_wound()
    survivor.take_wound()
    result = survivor.pick_up_equipment("Helmet")
    # A dead survivor cannot pick up equipment
    assert result == "Diana is dead"

def test_experience_and_level_up():
    survivor = Survivor("Eve")
    for _ in range(7):  # Kills 7 zombies
        survivor.earn_experience()
    # Each zombie killed earns the survivor one experience point
    assert survivor.experience == 7
    assert survivor.level == "Yellow"

    for _ in range(11):  # Kills 11 more zombies
        survivor.earn_experience()
    # Reaching Orange at 19 experience
    assert survivor.experience == 19
    assert survivor.level == "Orange"

def test_level_boundaries():
    survivor = Survivor("Frank")
    # Check boundary at Blue
    survivor.earn_experience()  # 1 XP
    assert survivor.level == "Blue"
    for _ in range(5):  # 5 more XP, total of 6
        survivor.earn_experience()
    assert survivor.level == "Blue"
    survivor.earn_experience()  # 7 XP
    assert survivor.level == "Yellow"

    # Check boundary at Orange
    for _ in range(11):  # 11 more XP, total of 18
        survivor.earn_experience()
    assert survivor.level == "Orange"
    survivor.earn_experience()  # 43 XP
    assert survivor.level == "Red"

def test_unlock_skills():
    survivor = Survivor("Frank")
    for _ in range(7):  # Kills 7 zombies
        survivor.earn_experience()
    # Below Yellow, no skills are available
    assert survivor.skills == []
    
    survivor.earn_experience()  # Reaching Yellow
    assert survivor.skills == ["+1 Action"]
    assert survivor.actions == 4

    survivor.earn_experience()  # Still Yellow
    assert survivor.skills == ["+1 Action"]
    assert survivor.choose_skill("Hoard") == "Frank has no skill choice available"  # No skills available to choose

    survivor.earn_experience()  # Reaching Orange for skill choices
    assert survivor.experience == 19  # Confirming XP is 19 before choosing
    assert survivor.choose_skill("Hoard") is None  # Valid choice, no return value specified
    assert survivor.skills == ["+1 Action", "Hoard"]
    
    # Check the carrying capacity increases
    assert survivor.carrying_capacity == 6  # Capacity increases to 6

def test_skill_choices_at_orange():
    survivor = Survivor("Gina")
    for _ in range(19):  # Kills 19 zombies
        survivor.earn_experience()
    
    # At Orange, should have two skills to pick from
    assert survivor.choose_skill("Hoard") is None  # Should succeed
    assert survivor.skills == ["+1 Action", "Hoard"]
    
    # Trying to choose a skill not available
    assert survivor.choose_skill("Tough") == "'Tough' is not an available skill choice"  # Invalid choice

def test_game_roster_and_end_condition():
    game = Game(fixed_clock)
    assert game.history == [f"Game started at {fixed_clock.isoformat()}"]

    survivor1 = Survivor("Grace")
    survivor2 = Survivor("Hank")
    game.add_survivor(survivor1)
    assert game.history == [f"Game started at {fixed_clock.isoformat()}", "Grace joined the game"]
    game.add_survivor(survivor2)
    assert game.history == [f"Game started at {fixed_clock.isoformat()}", "Grace joined the game", "Hank joined the game"]

    survivor1.take_wound()
    survivor1.take_wound()  # Grace dies
    assert game.is_over() is False
    
    survivor2.take_wound()
    survivor2.take_wound()  # Hank also dies
    assert game.is_over() is True
    assert game.history == [
        f"Game started at {fixed_clock.isoformat()}",
        "Grace joined the game",
        "Hank joined the game",
        "Grace was wounded",
        "Grace died",
        "Hank was wounded",
        "Hank died",
        "The game has ended: all survivors died"
    ]

def test_duplicate_survivor_names():
    game = Game(fixed_clock)
    survivor1 = Survivor("Alex")
    game.add_survivor(survivor1)
    
    survivor2 = Survivor("Alex")
    result = game.add_survivor(survivor2)
    assert result == "A survivor named 'Alex' already exists"

def test_dead_joiner_ends_game():
    game = Game(fixed_clock)
    survivor1 = Survivor("Zoe")
    game.add_survivor(survivor1)
    survivor1.take_wound()
    survivor1.take_wound()  # Zoe dies
    assert game.is_over() is True
    
    survivor2 = Survivor("DeadAlex")
    survivor2.take_wound()
    game.add_survivor(survivor2)  # Dead joiner should end the game
    assert game.is_over() is True
    assert game.history.count("The game has ended: all survivors died") == 1  # Only recorded once

def test_dead_joiner_after_game_end():
    game = Game(fixed_clock)
    survivor1 = Survivor("Zoe")
    survivor1.take_wound()
    survivor1.take_wound()  # Zoe dies
    
    game.add_survivor(survivor1)  # Add dead survivor
    assert game.is_over() is True
    
    survivor2 = Survivor("DeadAlex")
    survivor2.take_wound()
    game.add_survivor(survivor2)  # Adding dead survivor again
    assert game.history.count("The game has ended: all survivors died") == 1  # Still only recorded once

def test_game_level_from_living_survivors():
    game = Game(fixed_clock)
    survivor1 = Survivor("Survivor1")
    survivor2 = Survivor("Survivor2")
    
    game.add_survivor(survivor1)
    survivor1.earn_experience()  # Level up to Yellow
    assert game.level == "Yellow"
    
    game.add_survivor(survivor2)
    survivor2.earn_experience()  # Level up to Orange
    assert game.level == "Orange"
    
    survivor1.take_wound()
    survivor1.take_wound()  # Survivor1 dies
    assert game.level == "Orange"  # Survivor2 still alive at Orange

    survivor2.take_wound()
    survivor2.take_wound()  # Survivor2 dies
    assert game.level == "Blue"  # No survivors, level reverts to Blue

def test_history_equipment_acquisition():
    game = Game(fixed_clock)
    survivor = Survivor("Alice")
    game.add_survivor(survivor)
    survivor.pick_up_equipment("Baseball Bat")
    assert game.history[-1] == "Alice acquired Baseball Bat"

def test_history_survivor_level_up():
    game = Game(fixed_clock)
    survivor = Survivor("Bob")
    game.add_survivor(survivor)
    for _ in range(7):  # Kills 7 zombies
        survivor.earn_experience()
    assert game.history[-1] == "Bob advanced to Yellow"

def test_history_game_level_change():
    game = Game(fixed_clock)
    survivor1 = Survivor("Grace")
    survivor2 = Survivor("Hank")
    game.add_survivor(survivor1)
    game.add_survivor(survivor2)

    survivor1.earn_experience()  # Grace to Yellow
    assert game.history.count("Game level changed to Yellow") == 1

    survivor2.earn_experience()  # Hank to Yellow, no change
    assert game.history.count("Game level changed to Yellow") == 1  # No new entry

    survivor1.earn_experience()  # Grace to Orange
    assert game.history.count("Game level changed to Orange") == 1

def test_no_event_for_non_level_changing_kill():
    game = Game(fixed_clock)
    survivor = Survivor("Alice")
    game.add_survivor(survivor)
    survivor.earn_experience()  # 1 XP
    assert survivor.experience == 1  # Still Blue
    # No event should be announced
    assert len(game.history) == 1  # Only the game start record