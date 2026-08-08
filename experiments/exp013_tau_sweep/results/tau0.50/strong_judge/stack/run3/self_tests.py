import pytest
from solution import Stack, EmptyStackError, FullStackError

def test_newly_created_stack_is_empty():
    stack = Stack()  # A newly created stack
    assert stack.is_empty()  # AC-1.1: A newly created stack is empty.

def test_emptiness_tracks_contents():
    stack = Stack()
    stack.push(1)
    assert not stack.is_empty()  # Pushed one value, should not be empty. (AC-1.2)
    stack.pop()
    assert stack.is_empty()  # Popped the value, should be empty. (AC-1.2)
    
    stack.push(1)
    stack.push(2)
    assert not stack.is_empty()  # Pushed two values, should not be empty. (AC-1.2)
    stack.pop()
    assert not stack.is_empty()  # Popped one value, should still not be empty. (AC-1.2)

def test_popping_returns_values_in_reverse_order():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2  # Last pushed (2) should be returned first. (AC-1.3)
    assert stack.pop() == 1  # Next should be the first pushed (1). (AC-1.3)

def test_popping_empty_stack_fails():
    stack = Stack()
    with pytest.raises(EmptyStackError) as exc_info:  # Dedicated empty-stack error.
        stack.pop()
    assert str(exc_info.value) == "Cannot pop from empty stack"  # AC-2.1 and AC-2.2

def test_pushing_to_full_stack_fails():
    stack = Stack(1)  # Maximum capacity of 1
    stack.push(1)
    with pytest.raises(FullStackError) as exc_info:  # Dedicated full-stack error.
        stack.push(2)
    assert str(exc_info.value) == "Stack is full"  # AC-3.1 and AC-3.2

def test_capacity_of_zero_fails_first_push():
    stack = Stack(0)  # Maximum capacity of 0
    with pytest.raises(FullStackError) as exc_info:  # Dedicated full-stack error.
        stack.push(1)
    assert str(exc_info.value) == "Stack is full"  # AC-3.3

def test_negative_capacity_is_rejected():
    with pytest.raises(Exception) as exc_info:  # Rejection of negative capacity.
        stack = Stack(-1)  # Attempt to create stack with negative capacity
    assert str(exc_info.value) == "Capacity cannot be negative"  # AC-3.4

def test_distinct_empty_and_full_stack_errors():
    stack = Stack()
    with pytest.raises(EmptyStackError) as empty_exc_info:  # Dedicated empty-stack error.
        stack.pop()
    
    stack = Stack(1)  # Maximum capacity of 1
    stack.push(1)
    with pytest.raises(FullStackError) as full_exc_info:  # Dedicated full-stack error.
        stack.push(2)

    assert type(empty_exc_info.value) is not type(full_exc_info.value)  # Ensure distinct error types.