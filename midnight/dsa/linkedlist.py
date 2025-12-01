from dataclasses import dataclass
from typing import Self


@dataclass
class Node:
    element: int = 0
    next: Self | None = None


class LinkedList:
    def __init__(self):
        self.__count = 0
        self.__head: Node | None = None

    def append(self, element: int):
        node = Node(element=element)
        if self.__count == 0:
            self.__head = node
        else:
            last = self[self.__count - 1]
            last.next = node
        self.__count += 1

    def pop(self, index: int) -> Node:
        abs_index = abs(index)

        if abs_index >= self.__count and index != 0:
            raise IndexError("Index out of range")

        current = self.__head

        if abs_index == 0:
            self.__head = current.next
        else:
            previous = self[abs_index - 1]
            current = previous.next
            previous.next = current.next

        self.__count -= 1

        return current

    def insert(self, index: int, element: int):
        abs_index = abs(index)

        if abs_index >= self.__count and index != 0:
            raise IndexError("Index out of range")

        node = Node(element=element)

        if abs_index == 0:
            current = self.__head
            node.next = current
            self.__head = node
        else:
            previous = self[abs_index - 1]
            current = previous.next
            previous.next = node
            node.next = current

        self.__count += 1

    def extend(self, list: Self):
        if len(list) == 0:
            return

        last = self[self.__count - 1]
        first = list[0]

        last.next = first
        self.__count += len(list)

    def insert_after(self, index: int, element: int):
        abs_index = abs(index)

        if abs_index >= self.__count:
            raise IndexError("Index out of range")

        node = Node(element=element)
        current = self[abs_index]
        current_next = current.next

        current.next = node
        node.next = current_next

        self.__count += 1

    def insert_before(self, index: int, element: int):
        abs_index = abs(index)

        if abs_index >= self.__count and index != 0:
            raise IndexError("Index out of range")

        node = Node(element=element)

        previous = self[abs_index - 1]
        current = previous.next
        previous.next = node
        node.next = current

    def clear(self):
        self.__head = None
        self.__count = 0

    def get_head(self) -> Node | None:
        return self.__head

    def __bool__(self):
        return self.__count > 0

    def __len__(self):
        return self.__count

    def __setitem__(self, index: int, node: Node):
        "replace the item in the index with the given node"
        abs_index = abs(index)
        if abs_index >= self.__count and index != 0:
            raise IndexError("Index out of range")

        current = self.__head

        if abs_index == 0:
            node.next = current.next
            self.__head = node
        else:
            previous = self[abs_index - 1]
            current = previous.next
            node.next = current.next
            previous.next = node

    def __getitem__(self, index: int) -> Node:
        abs_index = abs(index)

        if abs_index >= self.__count and index != 0:
            raise IndexError("Index out of range")

        node = self.__head

        for _ in range(index):
            node = node.next

        return node

    def __str__(self):
        current = self.__head
        elements = []
        while current:
            elements.append(str(current.element))
            current = current.next
        return " -> ".join(elements)
