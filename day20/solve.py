from dataclasses import dataclass
from typing import Optional


def get_data(filepath="input"):
    return [int(val) for val in open(filepath, "r").read().splitlines()]


def test_data():
    return """1
2
-3
3
-2
0
4""".splitlines()


@dataclass
class Node:
    value: int
    prev: Optional['Node'] = None
    subs: Optional['Node'] = None

    def __iter__(self):
        node = self.subs
        while node:
            yield node
            node = node.subs
        

class CircularList:
    def __init__(self, arr):
        self.nodes = [Node(value) for value in arr]
        for i, node in enumerate(self.nodes):
            node.prev = self.nodes[(i - 1)]
            node.subs = self.nodes[(i + 1) % len(self.nodes)]

    def __iter__(self):
        return self.nodes.__iter__()

    def __len__(self):
        return len(self.nodes)

    def get(self, value):
        for node in self.nodes:
            if node.value == value:
                return node

        raise RuntimeError

    def mix(self, times = 1):
        def helper():
            for node in self.nodes:
                node.prev.subs, node.subs.prev = node.subs, node.prev
                prev, subs = node.prev, node.subs
                for _ in range(node.value % (len(self.nodes) - 1)):
                    prev, subs = prev.subs, subs.subs
                prev.subs, node.prev = node, prev
                node.subs, subs.prev = subs, node

        for _ in range(times):
            helper()


def part1(data=test_data()):
    nodes = CircularList([int(value) for value in data])
    nodes.mix()

    return sum(node.value 
               for i, node in zip(range(3000), nodes.get(0)) 
               if i % 1000 == 999)


def part2(data=test_data()):
    DECRYPTION_KEY = 811589153
    nodes = CircularList([int(value) * DECRYPTION_KEY for value in data])
    nodes.mix(10)

    return sum(node.value 
               for i, node in zip(range(3000), nodes.get(0)) 
               if i % 1000 == 999)

if __name__ == "__main__":
    print(part1())
    # print(part1(get_data()))
    print(part2())
    print(part2(get_data()))
