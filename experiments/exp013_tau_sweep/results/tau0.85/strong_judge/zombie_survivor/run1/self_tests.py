import pytest
from solution import Survivor, Game

# US-1: Track a survivor's wounds and life

def test_new_survivor():
    survivor = Survivor("Alice")
    assert survivor.name == "Alice"
    assert survivor.wounds == 0
    assert survivor.is_alive is True
    assert survivor.actions_per_turn == 3
    assert survivor.equipment == []
    assert survivor.experience == 0
    assert survivor.level == "Blue"

def test_survivor_one_wound_alive():
    survivor = Survivor("Bob")
    survivor.take_wound()
    assert survivor.is_alive is True

def test_survivor_two_wounds():
    survivor = Survivor("Charlie")
    survivor.take_wound()
    survivor.take_wound()
    assert survivor.is_alive is False

def test_survivor_third_wound_ignored():
    survivor = Survivor("David")
    survivor.take_wound()
    survivor.take_wound()
    survivor.take_wound()  # Third wound should be ignored
    assert survivor.wounds == 2

# US-2: Manage a survivor's equipment load

def test_pickup_equipment():
    survivor = Survivor("Eve")
    survivor.pick_up("Sword")
    assert survivor.equipment == ["Sword"]

def test_pickup_equipment_fills_hand_first():
    survivor = Survivor("Frank")
    survivor.pick_up("Gun")
    survivor.pick_up("Knife")
    assert survivor.equipment == ["Gun", "Knife"]

def test_pickup_equipment_limit():
    survivor = Survivor("Grace")
    for i in range(5):
        survivor.pick_up(f"Item{i}")
    assert survivor.equipment == [f"Item{i}" for i in range(5)]
    
    # Trying to pick up an extra item should show an error
    with pytest.raises(Exception, match="Grace cannot carry any more equipment"):
        survivor.pick_up("ExtraItem")

def test_wounds_reduce_carrying_capacity():
    survivor = Survivor("Heidi")
    for i in range(5):
        survivor.pick_up(f"Item{i}")  # Fill to capacity
    survivor.take_wound()  # Capacity reduced to 4
    with pytest.raises(Exception, match="Heidi cannot carry any more equipment"):
        survivor.pick_up("Item5")  # Fifth pickup should be refused
    survivor.pick_up("Item6")  # Should discard the first reserve item
    assert survivor.equipment == ["Item1", "Item2", "Item3", "Item4", "Item6"]

def test_dead_survivor_cannot_pickup():
    survivor = Survivor("Jack")
    survivor.take_wound()
    survivor.take_wound()
    with pytest.raises(Exception, match="Jack is dead"):
        survivor.pick_up("Item")

# US-3: Earn experience and level up

def test_kill_earn_experience():
    survivor = Survivor("Liam")
    survivor.kill_zombie()
    assert survivor.experience == 1

def test_survivor_level_up():
    survivor = Survivor("Mona")
    for _ in range(7):
        survivor.kill_zombie()
    assert survivor.level == "Yellow"

def test_survivor_level_from_experience():
    survivor = Survivor("Nina")
    experience_levels = [0, 6, 7, 18, 19, 42, 43]
    expected_levels = ["Blue", "Blue", "Yellow", "Yellow", "Orange", "Orange", "Red"]
    
    for exp, expected_level in zip(experience_levels, expected_levels):
        survivor.experience = exp
        assert survivor.level == expected_level

# US-4: Unlock and choose skills

def test_survivor_skill_unlocks():
    survivor = Survivor("Oscar")
    for _ in range(7):
        survivor.kill_zombie()
    assert survivor.actions_per_turn == 4  # "+1 Action" unlocked
    
    for _ in range(12):  # Reach Orange
        survivor.kill_zombie()
    available_skills = survivor.unlock_skills()
    assert available_skills == ["Hoard", "Sniper"]

def test_choose_skill():
    survivor = Survivor("Paul")
    for _ in range(43):  # Reach Red
        survivor.kill_zombie()
    survivor.choose_skill("Hoard")
    assert survivor.skills == ["Hoard"]

def test_invalid_skill_choice():
    survivor = Survivor("Quinn")
    for _ in range(43):
        survivor.kill_zombie()
    with pytest.raises(Exception, match="Quinn has no skill choice available"):
        survivor.choose_skill("InvalidSkill")  # Not available

def test_no_skill_choice_below_orange():
    survivor = Survivor("Rita")
    for _ in range(18):  # Reach Yellow
        survivor.kill_zombie()
    survivor.experience = 6  # Below Orange
    available_skills = survivor.unlock_skills()
    assert available_skills == []
    with pytest.raises(Exception, match="Rita has no skill choice available"):
        survivor.choose_skill("Hoard")  # Not available

def test_choose_hoard_at_orange():
    survivor = Survivor("Steve")
    for _ in range(19):  # Reach Orange
        survivor.kill_zombie()
    survivor.choose_skill("Hoard")
    assert survivor.carrying_capacity == 6  # Capacity should be increased

def test_red_offered_choices_after_sniper():
    survivor = Survivor("Tina")
    for _ in range(43):  # Reach Red
        survivor.kill_zombie()
    survivor.choose_skill("Sniper")
    available_skills = survivor.unlock_skills()
    assert available_skills == ["Hoard", "Tough"]

def test_second_automatic_action_at_50_xp():
    survivor = Survivor("Uma")
    for _ in range(50):  # Reach 50 XP
        survivor.kill_zombie()
    assert survivor.actions_per_turn == 5  # Second "+1 Action" should be granted

# US-5: Run the game roster, level, and end condition

def test_new_game_no_survivors():
    game = Game("2026-01-01T12:00:00")  # Example clock
    assert game.survivors == []
    assert game.history[0] == "Game started at 2026-01-01T12:00:00"

def test_survivor_join_game():
    game = Game("2026-01-01T12:00:00")
    game.join(Survivor("Rachel"))
    assert len(game.survivors) == 1
    assert game.history[1] == "Rachel joined the game"

def test_multiple_survivor_joins():
    game = Game("2026-01-01T12:00:00")
    game.join(Survivor("Steve"))
    game.join(Survivor("Tina"))
    assert len(game.survivors) == 2
    assert game.history[1] == "Steve joined the game"
    assert game.history[2] == "Tina joined the game"

def test_duplicate_survivor_name():
    game = Game("2026-01-01T12:00:00")
    game.join(Survivor("Steve"))
    with pytest.raises(Exception, match="A survivor named 'Steve' already exists"):
        game.join(Survivor("Steve"))

def test_game_over_condition():
    game = Game("2026-01-01T12:00:00")
    survivor = Survivor("Tina")
    game.join(survivor)
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    assert game.is_over() is True

def test_empty_game_not_over():
    game = Game("2026-01-01T12:00:00")
    assert game.is_over() is False

def test_living_survivor_keeps_game_active():
    game = Game("2026-01-01T12:00:00")
    survivor = Survivor("Uma")
    game.join(survivor)
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    assert game.is_over() is True
    survivor2 = Survivor("Vera")
    game.join(survivor2)
    assert game.is_over() is False

def test_dead_joiner_ends_game():
    game = Game("2026-01-01T12:00:00")
    survivor = Survivor("Wanda")
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    game.join(survivor)
    assert game.is_over() is True

def test_later_dead_joiner_does_not_record_ending():
    game = Game("2026-01-01T12:00:00")
    survivor = Survivor("Xander")
    game.join(survivor)
    survivor.take_wound()
    survivor.take_wound()  # Now dead
    assert game.is_over() is True
    dead_survivor = Survivor("Yasmin")
    dead_survivor.take_wound()
    dead_survivor.take_wound()  # Now dead
    game.join(dead_survivor)  # Joining again should not change the game status
    assert game.history.count("The game has ended: all survivors died") == 1

def test_game_level_from_survivors():
    game = Game("2026-01-01T12:00:00")
    survivor1 = Survivor("Yara")
    survivor2 = Survivor("Zack")
    game.join(survivor1)
    game.join(survivor2)
    assert game.level == "Blue"

    survivor1.kill_zombie()  # Should change survivor1's level
    survivor1.experience = 7  # Reach Yellow
    assert game.level == "Yellow"

def test_dead_survivor_excluded_from_game_level():
    game = Game("2026-01-01T12:00:00")
    survivor1 = Survivor("Yara")
    survivor2 = Survivor("Zack")
    game.join(survivor1)
    game.join(survivor2)
    survivor1.take_wound()
    survivor1.take_wound()  # Now dead
    survivor2.kill_zombie()  # Level up survivor2 to Yellow
    survivor2.experience = 7
    assert game.level == "Yellow"

# US-6: Keep a history and announce survivor events

def test_history_recording():
    game = Game("2026-01-01T12:00:00")
    survivor = Survivor("Alice")
    game.join(survivor)
    survivor.pick_up("Axe")
    survivor.take_wound()
    survivor.take_wound()  # Dead
    assert game.history == [
        "Game started at 2026-01-01T12:00:00",
        "Alice joined the game",
        "Alice acquired Axe",
        "Alice was wounded",
        "Alice died",
        "The game has ended: all survivors died"
    ]

def test_game_level_change_recorded():
    game = Game("2026-01-01T12:00:00")
    survivor = Survivor("Bob")
    game.join(survivor)
    for _ in range(7):
        survivor.kill_zombie()
    assert "Game level changed to Yellow" in game.history

def test_listener_events():
    game = Game("2026-01-01T12:00:00")
    survivor = Survivor("Cathy")
    game.join(survivor)
    events = []
    survivor.add_listener(lambda kind, message: events.append((kind, message)))
    
    survivor.pick_up("Gun")
    assert ("acquired", "Cathy acquired Gun") in events

    survivor.take_wound()
    assert ("wounded", "Cathy was wounded") in events

    for _ in range(7):
        survivor.kill_zombie()  # Should not announce anything
    assert ("level-up", "Cathy advanced to Yellow") not in events

    survivor.take_wound()
    survivor.take_wound()  # Dead
    assert ("wounded", "Cathy was wounded") not in events