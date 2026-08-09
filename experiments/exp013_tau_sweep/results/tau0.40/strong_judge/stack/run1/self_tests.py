# test_bounded_stack.py

import pytest
from solution import Stack  # Replace with the appropriate class name if needed

def test_new_stack_is_empty():
    # AC-1.1: A newly created stack is empty.
    stack = Stack()
    assert stack.is_empty()  # Expecting True

def test_push_and_pop_single_value():
    # AC-1.2: Emptiness tracks contents: pushing one value and popping it leaves the stack empty.
    stack = Stack()
    stack.push(1)
    assert not stack.is_empty()  # Expecting False
    stack.pop()
    assert stack.is_empty()  # Expecting True

def test_push_two_and_pop_one():
    # AC-1.2: Pushing two values and popping one leaves it non-empty.
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert not stack.is_empty()  # Expecting False
    stack.pop()
    assert not stack.is_empty()  # Expecting False

def test_pop_returns_values_in_reverse_order():
    # AC-1.3: Popping returns values in the reverse of the order they were pushed.
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2  # Last pushed should be first popped
    assert stack.pop() == 1  # Next should be the first pushed

def test_pop_empty_stack_fails():
    # AC-2.1: Popping an empty stack fails with a dedicated empty-stack error.
    stack = Stack()
    with pytest.raises(EmptyStackError) as exc_info:  # Assuming EmptyStackError is the dedicated error
        stack.pop()
    assert str(exc_info.value) == "Cannot pop from empty stack"  # AC-2.2: Exact message for empty stack

def test_push_on_full_stack_fails():
    # AC-3.1: A maximum capacity may be set at creation; pushing onto a stack already holding that many values fails.
    stack = Stack(capacity=1)
    stack.push(1)
    with pytest.raises(FullStackError) as exc_info:  # Assuming FullStackError is the dedicated error
        stack.push(2)
    assert str(exc_info.value) == "Stack is full"  # AC-3.2: Exact message for full stack

def test_capacity_zero_fails_first_push():
    # AC-3.3: A capacity of zero is valid — the very first push already fails as full.
    stack = Stack(capacity=0)
    with pytest.raises(FullStackError) as exc_info:  # Assuming FullStackError is the dedicated error
        stack.push(1)
    assert str(exc_info.value) == "Stack is full"  # AC-3.2: Exact message for full stack

def test_negative_capacity_rejected():
    # AC-3.4: A negative capacity is rejected at creation with the exact message "Capacity cannot be negative".
    with pytest.raises(ValueError) as exc_info:  # Assuming ValueError is raised for negative capacity
        stack = Stack(capacity=-1)
    assert str(exc_info.value) == "Capacity cannot be negative"  # Exact message for negative capacity

def test_underflow_and_overflow_errors_are_distinct():
    # Testing that underflow and overflow errors are distinct
    stack = Stack(capacity=1)
    stack.push(1)
    with pytest.raises(FullStackError):
        stack.push(2)  # This should raise a full stack error
    stack.pop()  # Now the stack is empty
    with pytest.raises(EmptyStackError):
        stack.pop()  # This should raise an empty stack error