"""
Name: <Your Name>
File: linked_stack_exercise.py
Description: A linked-list implementation of the Stack ADT for integers
    (DCS 229 Project 4, Classwork #5). Each value is stored in a Node, and
    the head of the list is the top of the stack, so push, pop, peek, and
    size all run in O(1) time. The stack has no fixed capacity; popping or
    peeking an empty stack returns -1. The file ends with the provided
    test suite.
Date: October 25, 2026
Collaborators: None
External resources: DAIADS textbook (Stacks page); Claude (Anthropic AI
    assistant) helped write the stack methods, type hints, and doc strings.
"""

import inspect


class Node:
    """A single link in the stack: one value plus a reference to the next node."""

    def __init__(self, value: int, next_node: "Node | None") -> None:
        """Create a node holding `value` that points to `next_node`."""
        self.value = value
        self.next = next_node


class IntStack:
    """A stack of integers backed by a singly linked list."""

    def __init__(self) -> None:
        """Create an empty stack."""
        self.head: Node | None = None
        self.count = 0

    def is_empty(self) -> bool:
        """Return True if the stack holds no values, otherwise False."""
        # the list has no nodes exactly when head is None
        return self.head is None

    def push(self, value: int) -> None:
        """Push `value` onto the top of the stack."""
        # the new node becomes the head and links to the old head
        self.head = Node(value, self.head)
        self.count += 1

    def pop(self) -> int:
        """Remove and return the value on top of the stack.

        Return -1 if the stack is empty.
        """
        # nothing to remove from an empty stack
        if self.head is None:
            return -1
        # save the top value, then unlink the head node
        value = self.head.value
        self.head = self.head.next
        self.count -= 1
        return value

    def peek(self) -> int:
        """Return the value on top of the stack without removing it.

        Return -1 if the stack is empty.
        """
        # nothing to look at on an empty stack
        if self.head is None:
            return -1
        return self.head.value

    def size(self) -> int:
        """Return the number of values currently on the stack."""
        # count is kept up to date by push and pop, so no traversal is needed
        return self.count

    def has_valid_structure_for_testing(self) -> bool:
        """Return True if the list has no cycle and its length matches count."""
        slow = self.head
        fast = self.head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return False
        reachable = 0
        node = self.head
        while node is not None:
            reachable += 1
            node = node.next
        return reachable == self.count


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
    """Test basic push, pop, peek, size, and is_empty behavior."""
    stack = IntStack()

    check(stack.is_empty(), True)
    check(stack.size(), 0)
    check(stack.pop(), -1)
    check(stack.peek(), -1)
    check(stack.size(), 0)

    stack.push(4)
    check(stack.is_empty(), False)
    check(stack.size(), 1)
    check(stack.peek(), 4)
    check(stack.size(), 1)

    stack.push(7)
    check(stack.size(), 2)
    check(stack.peek(), 7)

    stack.push(9)
    check(stack.size(), 3)
    check(stack.peek(), 9)
    check(stack.has_valid_structure_for_testing(), True)

    check(stack.pop(), 9)
    check(stack.size(), 2)
    check(stack.peek(), 7)

    stack.push(2)
    check(stack.size(), 3)
    check(stack.peek(), 2)

    check(stack.pop(), 2)
    check(stack.pop(), 7)
    check(stack.pop(), 4)
    check(stack.size(), 0)
    check(stack.is_empty(), True)
    check(stack.has_valid_structure_for_testing(), True)

    check(stack.pop(), -1)
    check(stack.peek(), -1)
    check(stack.size(), 0)

    stack.push(6)
    check(stack.is_empty(), False)
    check(stack.size(), 1)
    check(stack.peek(), 6)
    check(stack.pop(), 6)
    check(stack.size(), 0)
    check(stack.is_empty(), True)


def test_long_runs_and_repeated_reuse() -> None:
    """Repeatedly fill the stack with 200 values and empty it again."""
    stack = IntStack()
    for round_number in range(25):
        check(stack.is_empty(), True)
        for i in range(200):
            stack.push(round_number * 1000 + i)
            check(stack.size(), i + 1)
            check(stack.peek(), round_number * 1000 + i)
        for i in range(199, -1, -1):
            check(stack.pop(), round_number * 1000 + i)
            check(stack.size(), i)
        check(stack.pop(), -1)
        check(stack.is_empty(), True)


def test_large_aggregate_workload() -> None:
    """Push and then pop 100,000 values to check correctness at scale."""
    n = 100_000
    stack = IntStack()
    for value in range(n):
        stack.push(value)
    ok = (stack.size() == n and stack.peek() == n - 1
          and stack.has_valid_structure_for_testing())
    for value in range(n - 1, -1, -1):
        ok = stack.pop() == value and ok
    ok = stack.is_empty() and stack.has_valid_structure_for_testing() and ok
    check(ok, True)


test_stack()
test_long_runs_and_repeated_reuse()
test_large_aggregate_workload()

if failures:
    raise SystemExit(1)
