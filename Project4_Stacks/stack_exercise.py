"""
Name: <Your Name>
File: stack_exercise.py
Description: A fixed-size, array-based implementation of the Stack ADT for
    integers (DCS 229 Project 4, Classwork #3). Values are stored in a
    pre-allocated Python list, and the index of the top element is tracked
    so that push, pop, peek, and size all run in O(1) time. Pushing onto a
    full stack fails, and popping or peeking an empty stack returns -1.
    The file ends with the provided test suite.
Date: October 25, 2026
Collaborators: None
External resources: DAIADS textbook (Stacks page); Claude (Anthropic AI
    assistant) helped write the stack methods, type hints, and doc strings.
"""

import inspect


class IntStack:
    """A stack of integers backed by a fixed-size array."""

    def __init__(self, capacity: int) -> None:
        """Create an empty stack that can hold at most `capacity` values."""
        self.A = [0] * capacity
        self.top = -1

    def is_empty(self) -> bool:
        """Return True if the stack holds no values, otherwise False."""
        # top is -1 exactly when nothing is on the stack
        return self.top == -1

    def is_full(self) -> bool:
        """Return True if every slot of the array is in use, otherwise False."""
        # the stack is full when top sits at the last index of the array
        return self.top == len(self.A) - 1

    def push(self, value: int) -> bool:
        """Push `value` onto the top of the stack.

        Return True if the value was added, or False if the stack was
        already full (in which case the stack is left unchanged).
        """
        # a fixed-size stack cannot grow, so reject the push when it is full
        if self.is_full():
            return False
        # move top up one slot and store the new value there
        self.top += 1
        self.A[self.top] = value
        return True

    def pop(self) -> int:
        """Remove and return the value on top of the stack.

        Return -1 if the stack is empty.
        """
        # nothing to remove from an empty stack
        if self.is_empty():
            return -1
        # save the top value, then move top down so that slot is no longer used
        value = self.A[self.top]
        self.top -= 1
        return value

    def peek(self) -> int:
        """Return the value on top of the stack without removing it.

        Return -1 if the stack is empty.
        """
        # nothing to look at on an empty stack
        if self.is_empty():
            return -1
        return self.A[self.top]

    def size(self) -> int:
        """Return the number of values currently on the stack."""
        # indexes 0 through top are in use, which is top + 1 values
        return self.top + 1

    def used_values_for_testing(self) -> list[int]:
        """Return the values on the stack, from bottom to top (for tests)."""
        return self.A[:self.top + 1]


failures = 0


def check(actual: object, expected: object) -> None:
    """Print "pass" if `actual` equals `expected`; otherwise report a failure."""
    global failures
    if actual == expected:
        print("pass")
    else:
        line = inspect.currentframe().f_back.f_lineno
        failures += 1
        print(f"fail at test line {line}: expected {expected!r} but got {actual!r}")


def test_stack() -> None:
    """Test basic push, pop, peek, and size behavior on a small stack."""
    stack = IntStack(4)

    check(stack.size(), 0)
    check(stack.pop(), -1)
    check(stack.peek(), -1)
    check(stack.size(), 0)

    check(stack.push(4), True)
    check(stack.size(), 1)
    check(stack.peek(), 4)
    check(stack.size(), 1)

    check(stack.push(7), True)
    check(stack.size(), 2)
    check(stack.peek(), 7)

    check(stack.push(9), True)
    check(stack.size(), 3)
    check(stack.peek(), 9)

    check(stack.push(2), True)
    check(stack.size(), 4)
    check(stack.peek(), 2)

    check(stack.push(5), False)
    check(stack.used_values_for_testing(), [4, 7, 9, 2])
    check(stack.size(), 4)
    check(stack.peek(), 2)

    check(stack.pop(), 2)
    check(stack.size(), 3)

    check(stack.pop(), 9)
    check(stack.size(), 2)

    check(stack.push(6), True)
    check(stack.used_values_for_testing(), [4, 7, 6])
    check(stack.size(), 3)
    check(stack.peek(), 6)

    check(stack.pop(), 6)
    check(stack.size(), 2)

    check(stack.pop(), 7)
    check(stack.size(), 1)

    check(stack.pop(), 4)
    check(stack.size(), 0)

    check(stack.pop(), -1)
    check(stack.peek(), -1)
    check(stack.size(), 0)

def test_boundary_sizes_and_reuse() -> None:
    """Fill and empty stacks of several capacities, then reuse them."""
    for capacity in (1, 2, 5, 32):
        stack = IntStack(capacity)
        check(stack.is_empty(), True)
        check(stack.is_full(), False)
        for i in range(capacity):
            check(stack.push(1000 + i), True)
            check(stack.size(), i + 1)
            check(stack.peek(), 1000 + i)
        check(stack.is_full(), True)
        check(stack.push(9999), False)
        check(stack.size(), capacity)
        for i in range(capacity - 1, -1, -1):
            check(stack.pop(), 1000 + i)
            check(stack.size(), i)
        check(stack.is_empty(), True)
        check(stack.push(77), True)
        check(stack.pop(), 77)
        check(stack.is_empty(), True)


def test_large_aggregate_workload() -> None:
    """Push and then pop 100,000 values to check correctness at scale."""
    n = 100_000
    stack = IntStack(n)
    ok = True
    for value in range(n):
        ok = stack.push(value) and ok
    ok = stack.size() == n and stack.is_full() and stack.peek() == n - 1 and ok
    for value in range(n - 1, -1, -1):
        ok = stack.pop() == value and ok
    ok = stack.is_empty() and stack.size() == 0 and ok
    check(ok, True)


test_stack()
test_boundary_sizes_and_reuse()
test_large_aggregate_workload()

if failures:
    raise SystemExit(1)
