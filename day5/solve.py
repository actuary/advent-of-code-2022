from dataclasses import dataclass
from typing import Optional, Tuple, List, Iterator
from collections import deque


def get_data(filepath="input"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""".splitlines()


@dataclass
class Command:
    count: int
    from_stack: int
    to_stack: int


def parse_data(data=test_data()):
    data_it = iter(data)
    data_it, stacks = parse_stacks(data_it)
    commands = parse_commands(data_it)

    return stacks, commands


def parse_stacks(data_it) -> Tuple[Iterator, List[deque]]:
    row = next(data_it)
    stack_size = int((len(row)+1)/4)
    stacks = [deque() for _ in range(stack_size)]

    while row[1] != "1":
        for i, stack in enumerate(stacks):
            if (el:=row[i*4 + 1]) != " ":
                stack.append(el)
        row = next(data_it)
    
    for stack in stacks:
        stack.reverse()

    next(data_it)
    
    return data_it, stacks


def parse_commands(data_it):
    comps = (row.split(" ") for row in data_it)
    return [Command(*(int(row[1]), int(row[3])-1, int(row[5])-1)) for row in comps]


def move_in_order(command: Command, stacks: List[deque]) -> None:
    for _ in range(command.count):  
        stacks[command.to_stack].append(stacks[command.from_stack].pop())


def move_in_reverse(command: Command, stacks: List[deque]) -> None:
    temp_stack = deque()
    for _ in range(command.count):  
        temp_stack.append(stacks[command.from_stack].pop())
    for _ in range(command.count):  
        stacks[command.to_stack].append(temp_stack.pop())
       

def top_of_the_pops(stacks: List[deque]) -> str:
    return "".join([stack.pop() for stack in stacks])


def part1(data=test_data()):
    stacks, commands = parse_data(data)
    for command in commands:
        move_in_order(command, stacks)

    return top_of_the_pops(stacks)


def part2(data=test_data()):
    stacks, commands = parse_data(data)
    for command in commands:
        move_in_reverse(command, stacks)

    return top_of_the_pops(stacks)


if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))
