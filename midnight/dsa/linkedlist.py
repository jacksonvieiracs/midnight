from dataclasses import dataclass
from typing import Self


@dataclass
class Node:
    element: int = 0
    next: Self | None = None


class LinkedList:
    def __init__(self):
        self.count = 0
        self.head: Node | None = None

    def push(self, element: int):
        node = Node(element=element)
        if self.head is None:
            self.head = node
        else:
            head = self.head
            node.next = head
            self.head = node

        self.count += 1

    def insert(self, index: int, element: int):
        if index < 0 or index > self.count:
            raise IndexError("Index out of range")

        node = Node(element=element)

        if index == 0:
            current = self.head
            node.next = current
            self.head = node
        else:
            previous = self[index - 1]
            current = previous.next
            previous.next = node
            node.next = current

        self.count += 1

    def __bool__(self):
        return self.count > 0

    def __len__(self):
        return self.count

    def __getitem__(self, index: int) -> Node | None:
        if index < 0 or index >= self.count:
            raise IndexError("Index out of range")

        node = self.head

        for _ in range(index):
            node = node.next

        return node

    def __str__(self):
        current = self.head
        elements = []
        while current:
            elements.append(str(current.element))
            current = current.next
        return " -> ".join(elements)
