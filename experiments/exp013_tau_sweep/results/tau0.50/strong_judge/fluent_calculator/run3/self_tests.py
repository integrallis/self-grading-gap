from solution import Calculator

def test_seeding_calculator_sets_starting_value():
    calc = Calculator()
    calc.seed(10)
    assert calc.result() == 10  # Seeding with 10 sets the starting value

def test_chain_addition():
    calc = Calculator().seed(10).add(5).add(5)
    assert calc.result() == 20  # 10 + 5 + 5 = 20

def test_chain_subtraction():
    calc = Calculator().seed(10).subtract(3)
    assert calc.result() == 7  # 10 - 3 = 7

def test_chain_addition_and_subtraction():
    calc = Calculator().seed(10).add(5).subtract(3)
    assert calc.result() == 12  # 10 + 5 - 3 = 12

def test_chain_operations_return_self():
    calc = Calculator().seed(10)
    assert calc.add(5) is calc  # Adding returns the same calculator instance
    assert calc.subtract(3) is calc  # Subtracting returns the same calculator instance
    assert calc.undo() is calc  # Undo returns the same calculator instance
    assert calc.redo() is calc  # Redo returns the same calculator instance
    assert calc.save() is calc  # Save returns the same calculator instance

def test_ignored_second_seed():
    calc = Calculator().seed(10).seed(20)
    assert calc.result() == 10  # The second seed is ignored

def test_ignored_operations_before_seeding():
    calc = Calculator().add(5).subtract(3)
    assert calc.result() == 0  # No operations should be applied, result is 0

def test_result_of_unseeded_calculator():
    calc = Calculator()
    assert calc.result() == 0  # Unseeded calculator should report 0

def test_ignored_invalid_addition():
    calc = Calculator().seed(10).add(5.5)
    assert calc.result() == 10  # 5.5 is ignored, result remains 10

def test_ignored_invalid_subtraction():
    calc = Calculator().seed(10).subtract("three")
    assert calc.result() == 10  # "three" is ignored, result remains 10

def test_negative_seed():
    calc = Calculator().seed(-5)
    assert calc.result() == -5  # Seeding with -5 sets the value

def test_negative_addition():
    calc = Calculator().seed(10).add(-3)
    assert calc.result() == 7  # 10 + (-3) = 7

def test_negative_subtraction():
    calc = Calculator().seed(10).subtract(-3)
    assert calc.result() == 13  # 10 - (-3) = 13

def test_undo_reverts_last_operation():
    calc = Calculator().seed(10).add(5).undo()
    assert calc.result() == 10  # Undo should revert to 10

def test_multiple_undos():
    calc = Calculator().seed(10).add(5).subtract(3).undo().undo()
    assert calc.result() == 10  # Undoing twice should revert to 10

def test_undo_does_not_go_past_seed():
    calc = Calculator().seed(10).undo()
    assert calc.result() == 10  # Undo on seed should do nothing

def test_undo_on_unseeded_calculator():
    calc = Calculator().undo().seed(10)
    assert calc.result() == 10  # Undo should do nothing on unseeded calculator

def test_redo_after_undo():
    calc = Calculator().seed(10).add(5).subtract(2).undo().undo().redo()
    assert calc.result() == 15  # Redoing should bring back the last addition

def test_redo_with_no_undo():
    calc = Calculator().seed(10).redo()
    assert calc.result() == 10  # Redo with nothing undone should do nothing

def test_new_operation_after_undo_discards_redo():
    calc = Calculator().seed(10).add(5).undo().add(3)
    assert calc.result() == 13  # New operation after undo should discard redo

def test_redo_can_be_undone():
    calc = Calculator().seed(10).add(5).subtract(2).undo().undo().redo()
    assert calc.result() == 15  # Redone operation can be undone to revert back to 10
    calc.undo()
    assert calc.result() == 10  # Undoing the redone operation should return to 10

def test_save_seals_history():
    calc = Calculator().seed(10).add(5).undo().save()
    assert calc.result() == 10  # Result after save should be 10
    calc.redo()
    assert calc.result() == 10  # Redo should do nothing after save
    calc.undo()
    assert calc.result() == 10  # Undo should also do nothing after save

def test_new_operations_after_save():
    calc = Calculator().seed(10).add(5).save().add(3)
    assert calc.result() == 18  # New operations after save should be valid

def test_invalid_seed_ignored_but_valid_seed_applies():
    calc = Calculator().seed(5.5).seed(10)
    assert calc.result() == 10  # Invalid seed is ignored, valid seed applies

def test_invalid_operations_ignored():
    calc = Calculator().seed(10).add("five").subtract(2.5)
    assert calc.result() == 10  # Invalid operations should be ignored

def test_operations_ignored_before_seeding():
    calc = Calculator().add(5).subtract(3).seed(10)
    assert calc.result() == 10  # Operations before seeding should be ignored