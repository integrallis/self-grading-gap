import pytest
from solution import *  # Import everything, as the exact public names are not specified.

def test_newly_created_stack_is_empty():
    stack = Stack()  # Assuming the class is named Stack
    assert stack.is_empty()  # AC-1.1

def test_empty_stack_popping():
    stack = Stack()
    stack.push(1)
    stack.pop()
    assert stack.is_empty()  # AC-1.2

def test_non_empty_stack_after_one_push():
    stack = Stack()
    stack.push(1)
    assert not stack.is_empty()  # AC-1.2

def test_popping_returns_values_in_reverse_order():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    popped_value = stack.pop()
    assert popped_value == 2  # AC-1.3
    assert not stack.is_empty()  # After popping one, stack should not be empty

    popped_value = stack.pop()
    assert popped_value == 1  # AC-1.3
    assert stack.is_empty()  # Now it should be empty

def test_popping_empty_stack_fails():
    stack = Stack()
    with pytest.raises(Exception) as excinfo:  # AC-2.1
        stack.pop()
    assert str(excinfo.value) == "Cannot pop from empty stack"  # AC-2.2

def test_push_on_full_stack_fails():
    stack = Stack(1)  # AC-3.1
    stack.push(1)
    with pytest.raises(Exception) as excinfo:
        stack.push(2)  # Should fail as stack is full
    assert str(excinfo.value) == "Stack is full"  # AC-3.2

def test_capacity_of_zero():
    stack = Stack(0)  # AC-3.3
    with pytest.raises(Exception) as excinfo:
        stack.push(1)  # Should fail as capacity is zero
    assert str(excinfo.value) == "Stack is full"  # AC-3.2

def test_negative_capacity_is_rejected():
    with pytest.raises(Exception) as excinfo:
        Stack(-1)  # AC-3.4
    assert str(excinfo.value) == "Capacity cannot be negative"  # AC-3.4