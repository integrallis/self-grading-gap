import pytest
from solution import Tower, Jelly, attack_round

def test_tower_damage_lookup():
    # Test pure-color tower attacking jelly of the same color
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 1 Blue vs Blue: 2 to 5
    assert 2 <= damage <= 5

    tower = Tower(color='Red', level=2)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 2 Red vs Red: 5 to 9
    assert 5 <= damage <= 9

    # Test pure-color tower attacking jelly of the opposite color
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Red', health=10)
    damage = tower.attack(jelly)  # Level 1 Blue vs Red: 0
    assert damage == 0

    tower = Tower(color='Red', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 3 Red vs Blue: 2
    assert damage == 2

    # Test dual-color tower against pure-color jellies
    tower = Tower(color='BlueRed', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 1 BlueRed vs Blue: 2
    assert damage == 2

    # Test against dual-color jelly
    tower = Tower(color='Blue', level=2)
    jelly = Jelly(color='BlueRed', health=10)
    damage = tower.attack(jelly)  # Level 2 Blue vs BlueRed: 2 to 4
    assert 2 <= damage <= 4

    # Test invalid tower levels
    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 0"):
        Tower(color='Blue', level=0)

    with pytest.raises(ValueError, match="tower level must be between 1 and 4, got 5"):
        Tower(color='Red', level=5)

def test_jelly_health_tracking():
    jelly = Jelly(color='Blue', health=10)
    assert jelly.is_alive()  # Health is positive
    jelly.take_damage(5)
    assert jelly.health == 5
    jelly.take_damage(5)
    assert jelly.health == 0
    assert not jelly.is_alive()  # Jelly is now dead

    with pytest.raises(ValueError, match="Jelly is dead and cannot be attacked."):
        jelly.take_damage(1)  # Attempting to attack a dead jelly

def test_attack_rolls():
    tower = Tower(color='Blue', level=1)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 1 Blue vs Blue: 2 to 5
    assert 2 <= damage <= 5
    assert jelly.health == 10 - damage

    tower = Tower(color='Red', level=3)
    jelly = Jelly(color='Blue', health=10)
    damage = tower.attack(jelly)  # Level 3 Red vs Blue: 2
    assert damage == 2
    assert jelly.health == 10 - damage

def test_fight_rounds_with_log():
    tower1 = Tower(color='Blue', level=1)
    tower2 = Tower(color='Red', level=2)
    jelly1 = Jelly(color='Blue', health=10)
    jelly2 = Jelly(color='Red', health=8)
    log = attack_round([tower1, tower2], [jelly1, jelly2])

    assert len(log) == 2  # Two attacks
    assert log[0]['tower'] == 'Blue'
    assert log[0]['jelly'] == 'Blue'
    assert jelly1.health < 10  # Jelly 1 took damage

    assert log[1]['tower'] == 'Red'
    assert log[1]['jelly'] == 'Red'
    assert jelly2.health < 8  # Jelly 2 took damage

    # Simulate jellies dying
    jelly1.take_damage(10)
    log = attack_round([tower1, tower2], [jelly1, jelly2])
    assert len(log) == 1  # Only tower2 attacks jelly2
    assert log[0]['tower'] == 'Red'
    assert log[0]['jelly'] == 'Red'