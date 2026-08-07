import pytest
from solution import BoundedStack  # Adjust the import based on the actual implementation

def test_new_stack_is_empty():
    # A newly created stack is empty
    stack = BoundedStack()
    assert stack.is_empty() == True

def test_push_and_pop_single_value():
    # Pushing one value and popping it leaves the stack empty
    stack = BoundedStack()
    stack.push(1)
    assert stack.pop() == 1  # Popped value should be 1
    assert stack.is_empty() == True  # Stack should be empty now

def test_push_and_pop_two_values():
    # Pushing two values and popping one leaves it non-empty
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2  # Popped value should be 2
    assert stack.is_empty() == False  # Stack should not be empty

def test_pop_returns_values_in_reverse_order():
    # Popping returns values in reverse of the order they were pushed
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.pop() == 3  # Last pushed value
    assert stack.pop() == 2  # Next last pushed value
    assert stack.pop() == 1  # First pushed value

def test_pop_empty_stack_fails_with_dedicated_error():
    # Popping an empty stack fails with a dedicated empty-stack error
    stack = BoundedStack()
    with pytest.raises(Exception) as excinfo:
        stack.pop()
    assert str(excinfo.value) == "Cannot pop from empty stack"  # Exact failure message

def test_push_to_full_stack_fails_with_dedicated_error():
    # A maximum capacity may be set at creation; pushing onto a full stack fails
    stack = BoundedStack(capacity=1)
    stack.push(1)
    with pytest.raises(Exception) as excinfo:
        stack.push(2)
    assert str(excinfo.value) == "Stack is full"  # Exact failure message

def test_capacity_zero_fails_on_first_push():
    # A capacity of zero is valid — the very first push already fails as full
    stack = BoundedStack(capacity=0)
    with pytest.raises(Exception) as excinfo:
        stack.push(1)
    assert str(excinfo.value) == "Stack is full"  # Exact failure message

def test_negative_capacity_rejected_on_creation():
    # A negative capacity is rejected at creation with the exact message
    with pytest.raises(Exception) as excinfo:
        stack = BoundedStack(capacity=-1)
    assert str(excinfo.value) == "Capacity cannot be negative"  # Exact failure message

def test_unbounded_stack_accepts_pushes():
    # An unbounded stack (no capacity) should allow multiple pushes
    stack = BoundedStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.pop() == 3  # Last pushed value
    assert stack.pop() == 2  # Next last pushed value
    assert stack.pop() == 1  # First pushed value

def test_empty_and_full_errors_are_distinct():
    # Verify that empty stack and full stack errors are distinct
    stack_empty = BoundedStack()
    stack_full = BoundedStack(capacity=1)
    stack_full.push(1)

    with pytest.raises(Exception) as excinfo_empty:
        stack_empty.pop()
    with pytest.raises(Exception) as excinfo_full:
        stack_full.push(2)

    assert str(excinfo_empty.value) == "Cannot pop from empty stack"
    assert str(excinfo_full.value) == "Stack is full"
    assert type(excinfo_empty.value) is not type(excinfo_full.value)  # Validate different exception types