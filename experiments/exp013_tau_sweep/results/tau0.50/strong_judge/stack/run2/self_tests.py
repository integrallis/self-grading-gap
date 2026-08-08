import pytest
from solution import BoundedStack  # Assuming the implementation resides in solution.py

def test_newly_created_stack_is_empty():
    stack = BoundedStack()
    # Since we just created the stack, it should be empty
    assert stack.is_empty() is True

def test_pushing_one_value_leaves_stack_empty_after_pop():
    stack = BoundedStack()
    stack.push(1)
    stack.pop()
    # After pushing one value and then popping it, the stack should be empty
    assert stack.is_empty() is True

def test_pushing_two_values_and_popping_one_leaves_stack_non_empty():
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    stack.pop()
    # After pushing two values and popping one, the stack should not be empty
    assert stack.is_empty() is False

def test_popping_returns_values_in_reverse_order():
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    popped_value = stack.pop()
    # The most recently pushed value (2) should be popped first
    assert popped_value == 2

    popped_value = stack.pop()
    # The next popped value should be the one that was pushed first (1)
    assert popped_value == 1

def test_popping_empty_stack_fails():
    stack = BoundedStack()
    # Popping from an empty stack should raise an empty stack error
    with pytest.raises(Exception) as excinfo:
        stack.pop()
    assert str(excinfo.value) == "Cannot pop from empty stack"

def test_pushing_to_full_stack_fails():
    stack = BoundedStack(max_capacity=1)
    stack.push(1)
    # Pushing another value should raise a full stack error
    with pytest.raises(Exception) as excinfo:
        stack.push(2)
    assert str(excinfo.value) == "Stack is full"

def test_capacity_of_zero_is_valid():
    stack = BoundedStack(max_capacity=0)
    # Pushing to a stack with max capacity of 0 should raise a full stack error
    with pytest.raises(Exception) as excinfo:
        stack.push(1)
    assert str(excinfo.value) == "Stack is full"

def test_negative_capacity_is_rejected_at_creation():
    with pytest.raises(Exception) as excinfo:
        BoundedStack(max_capacity=-1)
    assert str(excinfo.value) == "Capacity cannot be negative"

def test_empty_pop_and_full_push_fail_with_dedicated_errors():
    stack = BoundedStack(max_capacity=1)

    # Check the empty stack pop error is distinct
    with pytest.raises(Exception) as excinfo_empty:
        stack.pop()
    assert str(excinfo_empty.value) == "Cannot pop from empty stack"

    # Check the full stack push error is distinct
    stack.push(1)
    with pytest.raises(Exception) as excinfo_full:
        stack.push(2)
    assert str(excinfo_full.value) == "Stack is full"

    # Assert that the exception types are distinct
    assert type(excinfo_empty.value) is not type(excinfo_full.value)