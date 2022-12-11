from dataclasses import dataclass
from typing import Optional, Tuple
from collections import deque, defaultdict, Counter

def get_data():
    return {
        0: Monkey(starting_items=[93, 54, 69, 66, 71], 
                  operation=lambda old: old * 3, 
                  modulus = 7,
                  choices = (7, 1)),
        1: Monkey(starting_items=[89, 51, 80, 66], 
                  operation=lambda old: old * 17, 
                  modulus = 19,
                  choices = (5, 7)),
        2: Monkey(starting_items=[90, 92, 63, 91, 96, 63, 64], 
                  operation=lambda old: old + 1, 
                  modulus = 13,
                  choices = (4, 3)),
        3: Monkey(starting_items=[65, 77], 
                  operation=lambda old: old + 2, 
                  modulus = 3,
                  choices = (4, 6)),
        4: Monkey(starting_items=[76, 68, 94], 
                  operation=lambda old: old * old, 
                  modulus = 2,
                  choices = (0, 6)),
        5: Monkey(starting_items=[86, 65, 66, 97, 73, 83], 
                  operation=lambda old: old + 8, 
                  modulus = 11,
                  choices = (2, 3)),
        6: Monkey(starting_items=[78], 
                  operation=lambda old: old + 6, 
                  modulus = 17,
                  choices = (0, 1)),
        7: Monkey(starting_items=[89, 57, 59, 61, 87, 55, 55, 88], 
                  operation=lambda old: old + 7, 
                  modulus = 5,
                  choices = (2, 5)),
    }


def test_data():
    return {
        0: Monkey(starting_items=[79, 98], 
                  operation=lambda old: old * 19, 
                  modulus = 23,
                  choices = (2, 3)),
        1: Monkey(starting_items=[54, 65, 75, 74], 
                  operation=lambda old: old + 6, 
                  modulus = 19,
                  choices = (2, 0)),
        2: Monkey(starting_items=[79, 60, 97], 
                  operation=lambda old: old * old, 
                  modulus = 13,
                  choices = (1, 3)),
        3: Monkey(starting_items=[74], 
                  operation=lambda old: old + 3, 
                  modulus = 17,
                  choices = (0, 1))
    }


class Monkey:
    def __init__(self, starting_items, operation, modulus, choices, divisor = 1):
        self.starting_items: deque = deque(starting_items)
        self.op = operation
        self.modulus = modulus
        self.choices = choices

    def test(self, worry: int, monkeys):
        choice = self.choices[0] if worry % self.modulus == 0 else self.choices[1]
        monkeys[choice].give(worry)

    def inspect(self, monkeys, overall_modulus, divisor = 3) -> None:
        while len(self.starting_items) > 0:
            worry = (self.op(self.starting_items.popleft()) % overall_modulus)//divisor
            self.test(worry, monkeys)

    def give(self, item) -> None:
        self.starting_items.append(item)

    def __repr__(self) -> str:
        return f"Monkey({repr(self.starting_items)})"

import functools
import operator

def part1(monkeys=test_data()):
    inspections = Counter()
    ROUNDS = 20
    overall_modulus = functools.reduce(
            operator.__mul__, 
            [monkey.modulus for monkey in monkeys.values()], 
            1
        )
    for round_no in range(ROUNDS):
        for monkey_no, monkey in monkeys.items():
            inspections[monkey_no] += len(monkey.starting_items)
            monkey.inspect(monkeys, overall_modulus, 3)
    most_active = inspections.most_common(2)
    return functools.reduce(lambda old, new: old * new[1], most_active, 1)


def part2(monkeys=test_data()):
    inspections = Counter()
    ROUNDS = 10000
    overall_modulus = functools.reduce(
            operator.__mul__, 
            [monkey.modulus for monkey in monkeys.values()], 
            1
        )
    for round_no in range(ROUNDS):
        for monkey_no, monkey in monkeys.items():
            inspections[monkey_no] += len(monkey.starting_items)
            monkey.inspect(monkeys, overall_modulus, 1)

    most_active = inspections.most_common(2)
    return functools.reduce(lambda old, new: old * new[1], most_active, 1)

if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))
