from solution import Calculator

def test_seeding_calculator():
    # Seeding the calculator with 10 should set the starting value to 10
    calc = Calculator().seed(10)
    assert calc.result() == 10  # expected: 10

def test_addition():
    # Seed 10, add 5, add 5 gives 20
    calc = Calculator().seed(10).add(5).add(5)
    assert calc.result() == 20  # expected: 10 + 5 + 5 = 20

def test_subtraction():
    # Seed 10, subtract 5 gives 5
    calc = Calculator().seed(10).subtract(5)
    assert calc.result() == 5  # expected: 10 - 5 = 5

def test_combined_operations():
    # Seed 10, add 5, subtract 2 gives 13
    calc = Calculator().seed(10).add(5).subtract(2)
    assert calc.result() == 13  # expected: 10 + 5 - 2 = 13

def test_fluid_chaining():
    # Seed 10, add 5, subtract 2 and check result
    calc = Calculator().seed(10).add(5).subtract(2)
    assert calc.result() == 13  # expected: 10 + 5 - 2 = 13

def test_invalid_second_seed():
    # Seed 10, seed 20 should still return 10
    calc = Calculator().seed(10).seed(20)
    assert calc.result() == 10  # expected: 10

def test_invalid_addition_before_seed():
    # Add 5 before seeding should be ignored, result is 0
    calc = Calculator().add(5)
    assert calc.result() == 0  # expected: 0

def test_invalid_subtraction_before_seed():
    # Subtract 5 before seeding should be ignored, result is 0
    calc = Calculator().subtract(5)
    assert calc.result() == 0  # expected: 0

def test_ignore_non_whole_number_seed():
    # Seed with a non-whole number (2.5) should be ignored, then valid seed (10) should be accepted
    calc = Calculator().seed(2.5).seed(10)
    assert calc.result() == 10  # expected: 10

def test_ignore_non_whole_number_addition():
    # Seed 10, add a non-whole number (2.5) should be ignored
    calc = Calculator().seed(10).add(2.5)
    assert calc.result() == 10  # expected: 10

def test_ignore_non_whole_number_subtraction():
    # Seed 10, subtract a non-whole number (2.5) should be ignored
    calc = Calculator().seed(10).subtract(2.5)
    assert calc.result() == 10  # expected: 10

def test_ignore_text_operand_addition():
    # Seed 10, add a string should be ignored
    calc = Calculator().seed(10).add("x")
    assert calc.result() == 10  # expected: 10

def test_ignore_text_operand_subtraction():
    # Seed 10, subtract a string should be ignored
    calc = Calculator().seed(10).subtract("y")
    assert calc.result() == 10  # expected: 10

def test_ignore_negative_seed():
    # Seed with a negative whole number (-5) should be valid
    calc = Calculator().seed(-5)
    assert calc.result() == -5  # expected: -5

def test_add_negative_operand():
    # Seed 10, add -3 should give 7
    calc = Calculator().seed(10).add(-3)
    assert calc.result() == 7  # expected: 10 + (-3) = 7

def test_subtract_negative_operand():
    # Seed 10, subtract -2 should give 12
    calc = Calculator().seed(10).subtract(-2)
    assert calc.result() == 12  # expected: 10 - (-2) = 12

def test_undo_operation():
    # Seed 10, add 5, then undo should revert to 10
    calc = Calculator().seed(10).add(5).undo()
    assert calc.result() == 10  # expected: 10

def test_multiple_undo():
    # Seed 10, add 5, subtract 2, undo twice should revert to 10
    calc = Calculator().seed(10).add(5).subtract(2).undo().undo()
    assert calc.result() == 10  # expected: 10

def test_undo_does_not_go_past_seed():
    # Seed 10, add 5, undo twice should still be at 10
    calc = Calculator().seed(10).add(5).undo().undo()
    assert calc.result() == 10  # expected: 10

def test_undo_on_unseeded_calculator():
    # Undo on an unseeded calculator should change nothing and result is 0
    calc = Calculator().undo()
    assert calc.result() == 0  # expected: 0

def test_undo_on_unseeded_calculator_later_seed():
    # Undo on an unseeded calculator does not prevent later seeding
    calc = Calculator().undo().seed(10)
    assert calc.result() == 10  # expected: 10

def test_redo_operation():
    # Seed 10, add 5, undo, redo should give 15
    calc = Calculator().seed(10).add(5).undo().redo()
    assert calc.result() == 15  # expected: 15

def test_redo_with_nothing_to_redo():
    # Seed 10, add 5, undo, redo, redo again should still give 15
    calc = Calculator().seed(10).add(5).undo().redo().redo()
    assert calc.result() == 15  # expected: 15

def test_new_operation_after_undo_discard_redo():
    # Seed 10, add 5, undo, then add 2 should discard the redo state
    calc = Calculator().seed(10).add(5).undo().add(2)
    assert calc.result() == 12  # expected: 10 + 2 = 12

def test_redo_after_new_operation():
    # Seed 10, add 5, undo, then add 2 should discard the redo state
    calc = Calculator().seed(10).add(5).undo().add(2).redo()
    assert calc.result() == 12  # expected: 10 + 2 = 12

def test_redo_worked_sequence():
    # Seed 10, add 5, subtract 2, undo twice, redo should give 15
    calc = Calculator().seed(10).add(5).subtract(2).undo().undo().redo()
    assert calc.result() == 15  # expected: 10 + 5 = 15

def test_save_seals_history():
    # Seed 10, add 5, save, undo should change nothing
    calc = Calculator().seed(10).add(5).save().undo()
    assert calc.result() == 15  # expected: 15

def test_save_with_pending_redo_history():
    # Seed 10, add 5, subtract 2, undo, save, redo should change nothing
    calc = Calculator().seed(10).add(5).subtract(2).undo().save().redo()
    assert calc.result() == 15  # expected: 15

def test_new_operations_after_save():
    # Seed 10, save, then add 5 should be accepted
    calc = Calculator().seed(10).save().add(5)
    assert calc.result() == 15  # expected: 10 + 5 = 15

def test_post_save_operations_form_fresh_history():
    # Seed 10, save, then add 2 should be accepted and undo should work
    calc = Calculator().seed(10).save().add(5).add(2).undo()
    assert calc.result() == 15  # expected: 10 + 5 = 15

def test_fluid_chaining_for_mutators():
    # Each mutator should return the same calculator instance
    calc = Calculator().seed(10)
    assert calc.seed(10) is calc  # expected: same instance
    assert calc.add(5) is calc  # expected: same instance
    assert calc.subtract(2) is calc  # expected: same instance
    assert calc.undo() is calc  # expected: same instance
    assert calc.redo() is calc  # expected: same instance
    assert calc.save() is calc  # expected: same instance

def test_text_seed_ignored():
    # Seed with text should be ignored, then valid seed applies
    calc = Calculator().seed("x").seed(10)
    assert calc.result() == 10  # expected: 10

def test_operations_before_seeding_ignored():
    # Operations before seeding should be ignored, result is the seed value
    calc = Calculator().add(5).subtract(2).seed(10)
    assert calc.result() == 10  # expected: 10