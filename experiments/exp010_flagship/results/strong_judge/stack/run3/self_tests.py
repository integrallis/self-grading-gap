import pytest
from solution import BoundedStack  # Assuming the class is named BoundedStack

def test_new_stack_is_empty():
    # A newly created stack is empty.
    stack = BoundedStack()
    assert stack.is_empty()  # is_empty() should return True

def test_empty_stack_pop_fails():
    # Popping an empty stack fails with a dedicated empty-stack error.
    stack = BoundedStack()
    with pytest.raises(Exception) as exc_info:  # Replace Exception with the specific empty-stack exception when implemented
        stack.pop()
    assert str(exc_info.value) == "Cannot pop from empty stack"

def test_push_and_pop():
    # Pushing one value and popping it leaves the stack empty.
    stack = BoundedStack()
    stack.push(1)
    assert not stack.is_empty()  # is_empty() should return False
    popped_value = stack.pop()
    assert popped_value == 1  # Popped value should be 1
    assert stack.is_empty()  # Stack should be empty again

def test_push_two_pop_one():
    # Pushing two values and popping one leaves it non-empty.
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    assert not stack.is_empty()  # is_empty() should return False
    popped_value = stack.pop()
    assert popped_value == 2  # Popped value should be 2
    assert not stack.is_empty()  # Stack should still be non-empty

def test_pop_returns_last_pushed_value():
    # Popping returns values in the reverse of the order they were pushed.
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.pop() == 3  # Should return 3
    assert stack.pop() == 2  # Should return 2
    assert stack.pop() == 1  # Should return 1

def test_full_stack_push_fails():
    # A maximum capacity may be set at creation; pushing onto a stack already holding that many values fails.
    stack = BoundedStack(2)
    stack.push(1)
    stack.push(2)
    with pytest.raises(Exception) as exc_info:  # Replace Exception with the specific full-stack exception when implemented
        stack.push(3)
    assert str(exc_info.value) == "Stack is full"

def test_zero_capacity_stack_push_fails():
    # A capacity of zero is valid — the very first push already fails as full.
    stack = BoundedStack(0)
    with pytest.raises(Exception) as exc_info:  # Replace Exception with the specific full-stack exception when implemented
        stack.push(1)
    assert str(exc_info.value) == "Stack is full"

def test_negative_capacity_rejected():
    # A negative capacity is rejected at creation with the exact message "Capacity cannot be negative".
    with pytest.raises(Exception) as exc_info:  # Replace Exception with the specific exception when implemented
        BoundedStack(-1)
    assert str(exc_info.value) == "Capacity cannot be negative"

def test_distinct_exceptions_for_empty_and_full_stack():
    # Ensure that the empty-stack and full-stack exceptions are distinct.
    stack = BoundedStack(2)
    stack.push(1)
    stack.push(2)
    
    with pytest.raises(Exception) as full_error:  # Replace Exception with the specific full-stack exception when implemented
        stack.push(3)
    with pytest.raises(Exception) as empty_error:  # Replace Exception with the specific empty-stack exception when implemented
        stack.pop()
        stack.pop()
        stack.pop()  # This should pop the third element, causing an empty stack error.

    assert str(full_error.value) == "Stack is full"
    assert str(empty_error.value) == "Cannot pop from empty stack"
    assert type(empty_error.value) is not type(full_error.value)  # Ensure they are distinct exceptions.