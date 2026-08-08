from solution import Calculator

def test_seeding_calculator_sets_starting_value():
    # Seed 10, so result should be 10.
    calc = Calculator().seed(10)
    assert calc.result() == 10

def test_chaining_additions_increases_value():
    # Seed 10, add 5, add 5: 10 + 5 + 5 = 20.
    calc = Calculator().seed(10).add(5).add(5)
    assert calc.result() == 20

def test_chaining_subtractions_decreases_value():
    # Seed 10, subtract 5: 10 - 5 = 5.
    calc = Calculator().seed(10).subtract(5)
    assert calc.result() == 5

def test_combining_additions_and_subtractions():
    # Seed 10, add 5, subtract 3: 10 + 5 - 3 = 12.
    calc = Calculator().seed(10).add(5).subtract(3)
    assert calc.result() == 12

def test_chain_returns_same_calculator_instance():
    # Chain calls and check if the same instance is returned.
    calc = Calculator()
    assert calc.seed(10) is calc.add(5) is calc.subtract(3) is calc.undo() is calc.redo() is calc.save()

def test_invalid_second_seed_is_ignored():
    # Seed 10, then seed 20: should still be 10.
    calc = Calculator().seed(10).seed(20)
    assert calc.result() == 10

def test_invalid_addition_before_seeding_ignored():
    # Invalid addition before seeding: should return 0.
    calc = Calculator().add(5)
    assert calc.result() == 0

def test_unseeded_calculator_reports_zero():
    # Unseeded calculator: should return 0.
    calc = Calculator()
    assert calc.result() == 0

def test_invalid_addition_with_non_whole_number_ignored():
    # Seed 10, then add a float: should still be 10.
    calc = Calculator().seed(10).add(5.5)
    assert calc.result() == 10

def test_invalid_subtraction_with_text_operand_ignored():
    # Seed 10, then subtract a string: should still be 10.
    calc = Calculator().seed(10).subtract("invalid")
    assert calc.result() == 10

def test_invalid_subtraction_with_non_whole_number_ignored():
    # Seed 10, then subtract a float: should still be 10.
    calc = Calculator().seed(10).subtract(5.5)
    assert calc.result() == 10

def test_seed_with_negative_number_is_valid():
    # Seed -10, add 5: -10 + 5 = -5.
    calc = Calculator().seed(-10).add(5)
    assert calc.result() == -5

def test_negative_operand_is_valid():
    # Seed 10, subtract -5: 10 - (-5) = 15.
    calc = Calculator().seed(10).subtract(-5)
    assert calc.result() == 15

def test_undo_reverts_last_operation():
    # Seed 10, add 5, then undo: should revert to 10.
    calc = Calculator().seed(10).add(5).undo()
    assert calc.result() == 10

def test_undo_reverts_subtraction():
    # Seed 10, subtract 5, then undo: should revert to 10.
    calc = Calculator().seed(10).subtract(5).undo()
    assert calc.result() == 10

def test_multiple_undos_revert_history():
    # Seed 10, add 5, subtract 3, two undos: should revert to 10.
    calc = Calculator().seed(10).add(5).subtract(3).undo().undo()
    assert calc.result() == 10

def test_undo_does_not_revert_past_seed():
    # Seed 10, add 5, then undo twice: should revert to 10.
    calc = Calculator().seed(10).add(5).undo().undo()
    assert calc.result() == 10

def test_undo_on_unseeded_calculator_changes_nothing():
    # Unseeded calculator, performing undo: should still be 0.
    calc = Calculator().undo()
    assert calc.result() == 0

def test_undo_on_unseeded_calculator_does_not_block_later_seed():
    # Unseeded calculator, performing undo, then seed 10: should be 10.
    calc = Calculator().undo().seed(10)
    assert calc.result() == 10

def test_redo_reapplies_last_undone_operation():
    # Seed 10, add 5, subtract 2, then two undos, then redo: should be 15.
    calc = Calculator().seed(10).add(5).subtract(2).undo().undo().redo()
    assert calc.result() == 15

def test_redo_with_nothing_undone_changes_nothing():
    # Seed 10, add 5, then redo without undo: should still be 15.
    calc = Calculator().seed(10).add(5).redo()
    assert calc.result() == 15

def test_new_operation_after_undo_discards_redo_history():
    # Seed 10, add 5, then undo, then add 3: should be 13, then redo should still be 13.
    calc = Calculator().seed(10).add(5).undo().add(3)
    assert calc.result() == 13
    calc.redo()
    assert calc.result() == 13

def test_redone_operation_can_be_undone_again():
    # Seed 10, add 5, subtract 2, then undo, redo, then undo: should revert to 15.
    calc = Calculator().seed(10).add(5).subtract(2).undo().redo().undo()
    assert calc.result() == 15

def test_save_seals_history():
    # Seed 10, add 5, save: should be 15, undo should change nothing.
    calc = Calculator().seed(10).add(5).save().undo()
    assert calc.result() == 15

def test_new_operations_after_save_build_fresh_history():
    # Seed 10, save, then add 5: should be 15.
    calc = Calculator().seed(10).save().add(5)
    assert calc.result() == 15

def test_redo_after_save_changes_nothing():
    # Seed 10, save, then redo should change nothing.
    calc = Calculator().seed(10).save().redo()
    assert calc.result() == 10

def test_save_while_redo_history_pending():
    # Seed 10, add 5, undo, save: should be 10, undo and redo should change nothing.
    calc = Calculator().seed(10).add(5).undo().save()
    assert calc.result() == 10
    calc.undo()
    assert calc.result() == 10
    calc.redo()
    assert calc.result() == 10

def test_operation_made_after_save_can_be_undone():
    # Seed 10, save, then add 5 and undo: should revert to 10.
    calc = Calculator().seed(10).save().add(5).undo()
    assert calc.result() == 10