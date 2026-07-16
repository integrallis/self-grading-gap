from solution import Calculator

def test_seeding_calculator_sets_initial_value():
    calc = Calculator()
    calc.seed(10)
    result = calc.result()  # Should return 10
    assert result == 10

def test_chaining_additions_increases_value():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).add(5)
    result = calc.result()  # Should return 20 (10 + 5 + 5)
    assert result == 20

def test_chaining_subtractions_decreases_value():
    calc = Calculator()
    calc.seed(10)
    calc.subtract(3).subtract(2)
    result = calc.result()  # Should return 5 (10 - 3 - 2)
    assert result == 5

def test_chaining_additions_and_subtractions():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).subtract(2).add(3)
    result = calc.result()  # Should return 16 (10 + 5 - 2 + 3)
    assert result == 16

def test_chain_fluidity():
    calc = Calculator()
    result = calc.seed(10).add(5).subtract(2).result()  # Should return 13
    assert result == 13

def test_invalid_seed_is_ignored():
    calc = Calculator()
    calc.seed(10)
    calc.seed(20)  # This should be ignored
    result = calc.result()  # Should still return 10
    assert result == 10

def test_invalid_operations_before_seeding():
    calc = Calculator()
    calc.add(5)  # This should be ignored
    result = calc.result()  # Should return 0 because it is unseeded
    assert result == 0

def test_unseeded_calculator_reports_zero():
    calc = Calculator()
    result = calc.result()  # Should return 0 without raising
    assert result == 0

def test_invalid_addition_with_non_whole_number():
    calc = Calculator()
    calc.seed(10)
    calc.add(5.5)  # This should be ignored
    result = calc.result()  # Should return 10
    assert result == 10

def test_negative_seed_is_valid():
    calc = Calculator()
    calc.seed(-10)
    result = calc.result()  # Should return -10
    assert result == -10

def test_undo_reverts_most_recent_operation():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).subtract(2)
    calc.undo()
    result = calc.result()  # Should return 13 (10 + 5)
    assert result == 13

def test_repeated_undo_steps_back_through_history():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).subtract(2)
    calc.undo().undo()
    result = calc.result()  # Should return 10
    assert result == 10

def test_undo_does_not_revert_past_seed():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo().undo()  # Should have no effect beyond seed
    result = calc.result()  # Should return 10
    assert result == 10

def test_undo_on_unseeded_calculator_changes_nothing():
    calc = Calculator()
    calc.undo()  # This should change nothing
    result = calc.result()  # Should return 0
    assert result == 0

def test_redo_reapplies_most_recently_undone_operation():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.redo()
    result = calc.result()  # Should return 15 (10 + 5)
    assert result == 15

def test_redo_with_nothing_undone_changes_nothing():
    calc = Calculator()
    calc.seed(10)
    calc.redo()  # This should change nothing
    result = calc.result()  # Should return 10
    assert result == 10

def test_new_operation_after_undo_discards_redo_history():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.add(3)  # New operation after undo
    calc.redo()  # This should change nothing
    result = calc.result()  # Should return 13 (10 + 3)
    assert result == 13

def test_redone_operation_can_be_undone_again():
    calc = Calculator()
    calc.seed(10)
    calc.add(5)
    calc.undo()
    calc.redo()
    calc.undo()
    result = calc.result()  # Should return 10
    assert result == 10

def test_save_seals_the_history():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).save()
    calc.add(3)  # New operation after save
    result = calc.result()  # Should return 13 (10 + 3)
    assert result == 13
    calc.undo()  # Should have no effect as history is sealed
    result_after_undo = calc.result()  # Should still return 13
    assert result_after_undo == 13

def test_save_prevents_redo_of_previous_operations():
    calc = Calculator()
    calc.seed(10)
    calc.add(5).save()
    calc.undo()  # Undoing before save
    calc.redo()  # This should change nothing
    result = calc.result()  # Should still return 10
    assert result == 10